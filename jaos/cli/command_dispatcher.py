from jaos.ai import (
    AIManager,
    AIProviderConfig,
    AIProviderType,
    ProviderManager,
)
from jaos.ai.diagnostics import DiagnosticStatus as AIDiagnosticStatus
from jaos.ai.intelligence import ProviderProfileRegistry
from jaos.ai.operations import ProviderStatusService
from jaos.ai.providers.mock_provider import MockProvider
from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.executive.diagnostics.models import (
    DiagnosticStatus as ExecutiveDiagnosticStatus,
)
from jaos.tools.tool_manager import ToolManager


class CommandDispatcher:
    """
    Routes JAOS shell commands.
    """

    def __init__(self, tool_manager: ToolManager | None = None) -> None:
        self.tool_manager = tool_manager or ToolManager()

        load_tools(self.tool_manager)

        self.ai_manager = self._build_ai_manager()
        self.provider_profiles = ProviderProfileRegistry.build_default()
        self.provider_status = ProviderStatusService(
            self.ai_manager.get_provider_manager()
        )
        self.executive = ExecutiveController(
            self.tool_manager,
            ai_manager=self.ai_manager,
        )

    def shutdown(self) -> None:
        """
        Synchronously shut down AI provider lifecycle owned by this dispatcher.

        Delegates to AIManager.shutdown(); does not access concrete providers
        and does not catch shutdown errors.
        """
        self.ai_manager.shutdown()

    def dispatch(self, command: str) -> bool:
        normalized = command.strip().lower()

        if normalized == "help":
            self._show_help()
            return True

        if normalized == "status":
            self._show_status()
            return True

        if normalized == "identity":
            self._show_identity()
            return True

        if normalized == "providers":
            self._show_providers()
            return True

        if normalized == "status executive":
            self._show_executive_status()
            return True

        if normalized == "status ai":
            self._show_ai_status()
            return True

        if normalized == "metrics executive":
            self._show_executive_metrics()
            return True

        if normalized == "metrics ai":
            self._show_ai_metrics()
            return True

        if normalized == "tools":
            self._show_tools()
            return True

        if normalized == "ai" or normalized.startswith("ai "):
            self._handle_ai_command(command[2:].strip())
            return True

        if normalized == "exit":
            print("Shutting down JAOS...")
            self.shutdown()
            return False

        usage = self._incomplete_filesystem_usage(command)
        if usage is not None:
            print()
            print(usage)
            print()
            return True

        response = self.executive.process(command)

        print()

        if response.success:
            print(response.message)

            if response.output is not None:
                if isinstance(response.output, dict):
                    content = response.output.get("content")
                    matches = response.output.get("matches")

                    if content is not None:
                        print()
                        print(content)
                    elif matches is not None:
                        print()
                        for match in matches:
                            print(match)
                    else:
                        provider = response.output.get("provider")
                        if provider is not None:
                            print(f"Provider: {provider}")
                else:
                    print(response.output)
        else:
            print(response.message)

        print()

        return True

    def _build_ai_manager(self) -> AIManager:
        provider_manager = ProviderManager()

        provider_manager.register_provider(
            MockProvider(),
            AIProviderConfig(
                name="mock",
                provider_type=AIProviderType.MOCK,
                default_model="mock-model",
            ),
            set_default=True,
        )

        provider_manager.initialize_provider("mock")

        return AIManager(provider_manager)

    def _handle_ai_command(self, prompt: str) -> None:
        print()

        if not prompt:
            print("AI prompt cannot be empty.")
            print()
            return

        response = self.ai_manager.generate(prompt)

        print(response.text)
        print()

    @staticmethod
    def _incomplete_filesystem_usage(command: str) -> str | None:
        """
        Return usage guidance for documented incomplete filesystem shell forms.

        Only the proven incomplete shapes listed for SHT-006 are intercepted.
        Complete forms, delete-with-path, unknown commands, and free-form text
        return None so existing Executive/AI routing remains unchanged.
        """
        parts = command.strip().split()

        if not parts:
            return None

        verb = parts[0].lower()
        argument_count = len(parts) - 1

        if verb == "read" and argument_count == 0:
            return "Usage: read <path>"

        if verb == "write" and argument_count < 2:
            return "Usage: write <path> <content>"

        if verb == "copy" and argument_count < 2:
            return "Usage: copy <source> <destination>"

        if verb == "move" and argument_count < 2:
            return "Usage: move <source> <destination>"

        if verb == "rename" and argument_count < 2:
            return "Usage: rename <source> <new_name>"

        if verb == "delete" and argument_count == 0:
            return "Usage: delete <path> --confirm"

        if verb == "search" and argument_count < 2:
            return "Usage: search <root> <pattern>"

        if verb == "backup" and argument_count < 2:
            return "Usage: backup <source> <destination>"

        return None

    def _show_help(self) -> None:
        print()
        print("Available commands")
        print("------------------")
        print("help               - Show this help")
        print("status             - Show JAOS system status")
        print("identity           - Show JAOS identity")
        print("providers          - Show known AI provider profiles")
        print("status executive   - Show Executive Platform status")
        print("status ai          - Show AI Platform status")
        print("metrics executive  - Show Executive Platform metrics")
        print("metrics ai         - Show AI Platform metrics")
        print("tools              - Show registered JAOS tools")
        print("ai <prompt>        - Send prompt to AI Platform")
        print("read <path>        - Read a UTF-8 text file")
        print("write <path> <content>")
        print("copy <source> <destination>")
        print("move <source> <destination>")
        print("rename <source> <new_name>")
        print("delete <path> --confirm")
        print("search <root> <pattern>")
        print("backup <source> <destination>")
        print("exit               - Exit JAOS")
        print()

    def _show_status(self) -> None:
        ai_status = self.ai_manager.get_status()
        ai_diagnostic = self.ai_manager.get_diagnostic_status()
        executive_status = self.executive.get_status()
        registered_tools = self.tool_manager.list_tools()

        print()
        print("System Status")
        print("-------------")
        print("Boot: Online")
        print("Shell: Online")
        print(
            "Executive Controller: "
            + ("Online" if executive_status.healthy else "Degraded")
        )
        print("Command Dispatcher: Online")
        print(
            "Tool Platform: "
            + ("Ready" if registered_tools else "Not Ready")
        )
        print(
            "AI Platform: "
            + ("Ready" if ai_diagnostic.healthy else "Not Ready")
        )
        print(f"AI Providers: {ai_status.provider_count}")
        print(f"Default AI Provider: {ai_status.default_provider}")
        print(f"Registered Tools: {len(registered_tools)}")
        print()

    def _show_identity(self) -> None:
        identity = self.ai_manager.get_identity_manager().get_identity()

        print()
        print("JAOS Identity")
        print("-------------")
        print(f"Name: {identity.name}")
        print(f"Codename: {identity.codename}")
        print(f"Version: {identity.version}")
        print()
        print("Description")
        print("-----------")
        print(identity.description)
        print()
        print("Capabilities")
        print("------------")

        for capability in identity.capabilities:
            print(f"- {capability.name}: {capability.description}")

        print()
        print("Limitations")
        print("-----------")

        for limitation in identity.limitations:
            print(f"- {limitation.name}: {limitation.description}")

        print()

    def _show_providers(self) -> None:
        statuses = {
            status.name: status
            for status in self.provider_status.list_provider_statuses()
        }

        print()
        print("Known AI Providers")
        print("------------------")

        for profile in self.provider_profiles.list_profiles():
            status = statuses.get(profile.name)

            print()
            print(profile.display_name)
            print("-" * len(profile.display_name))
            print(f"Name: {profile.name}")
            print(f"Cost: {profile.cost_type.value}")
            print(f"Privacy: {profile.privacy_type.value}")
            print(f"Description: {profile.description}")

            print()
            print("Operational Status")
            print("------------------")

            if status is None:
                print("Configured: No")
                print("Enabled: No")
                print("Default: No")
                print("Secret Required: Unknown")
                print("Secret Present: Unknown")
                print("Current Model: None")
            else:
                print(f"Configured: {self._yes_no(status.configured)}")
                print(f"Enabled: {self._yes_no(status.enabled)}")
                print(f"Default: {self._yes_no(status.is_default)}")
                print(f"Secret Required: {self._yes_no(status.secret_required)}")
                print(f"Secret Present: {self._yes_no(status.secret_present)}")
                print(f"Current Model: {status.current_model}")

            print()
            print("Strengths")
            print("---------")
            for strength in profile.strengths:
                print(f"- {strength}")

            print()
            print("Limitations")
            print("-----------")
            for limitation in profile.limitations:
                print(f"- {limitation}")

            print()
            print("Recommended For")
            print("---------------")
            for item in profile.recommended_for:
                print(f"- {item}")

        print()

    def _show_ai_status(self) -> None:
        status = self.ai_manager.get_diagnostic_status()
        self._print_ai_diagnostic_status(status)

    def _show_ai_metrics(self) -> None:
        metrics = self.ai_manager.get_metrics()

        print()
        print("AI Metrics")
        print("----------")
        print(f"Requests Total: {metrics.requests_total}")
        print(f"Requests Succeeded: {metrics.requests_succeeded}")
        print(f"Requests Failed: {metrics.requests_failed}")
        print(f"Success Rate: {metrics.success_rate():.2%}")
        print(f"Last Provider: {metrics.last_provider}")
        print(f"Last Model: {metrics.last_model}")
        print()

    def _show_executive_status(self) -> None:
        status = self.executive.get_status()
        self._print_executive_diagnostic_status(status)

    def _show_executive_metrics(self) -> None:
        metrics = self.executive.get_metrics()

        print()
        print("Executive Metrics")
        print("-----------------")
        print(f"Plans Executed: {metrics.plans_executed}")
        print(f"Plans Succeeded: {metrics.plans_succeeded}")
        print(f"Plans Failed: {metrics.plans_failed}")
        print(f"Last Plan Steps: {metrics.last_plan_steps}")
        print(f"Success Rate: {metrics.success_rate():.2%}")
        print()

    def _show_tools(self) -> None:
        print()
        print("Registered Tools")
        print("----------------")

        tools = self.tool_manager.list_tools()

        if not tools:
            print("No tools registered.")
        else:
            for tool in tools:
                print(f"- {tool}")

        print()

    def _print_ai_diagnostic_status(self, status: AIDiagnosticStatus) -> None:
        print()
        print(status.component)
        print("-" * len(status.component))
        print(f"Healthy: {status.healthy}")
        print(f"Message: {status.message}")
        print(f"Provider Count: {status.details.get('provider_count')}")
        print(f"Default Provider: {status.details.get('default_provider')}")

        providers = status.details.get("providers", ())

        if providers:
            print()
            print("Providers")
            print("---------")
            for provider in providers:
                print(f"- {provider}")

        print()

    def _print_executive_diagnostic_status(
        self,
        status: ExecutiveDiagnosticStatus,
    ) -> None:
        print()
        print(status.component)
        print("-" * len(status.component))
        print(f"Healthy: {status.healthy}")
        print(f"Message: {status.message}")

        handlers = status.details.get("handlers", {})
        handler_names = handlers.get("handlers", ())

        if handler_names:
            print()
            print("Handlers")
            print("--------")
            for handler in handler_names:
                print(f"- {handler}")

        print()

    @staticmethod
    def _yes_no(value: bool) -> str:
        return "Yes" if value else "No"