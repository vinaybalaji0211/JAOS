"""FORTRESS-05: the canonical whole-system composition root.

Composes the real AI, Tool, Executive, Memory, and Conversation Intelligence
platforms into a PlatformRuntime that has already reached READY, registering
each canonical service so PlatformRuntime's own container/registry are the
single authoritative record of what is live. CommandDispatcher receives its
Tool, AI, and Executive collaborators from this composition root and performs
no independent platform construction.

Memory composition uses the canonical modern chain exclusively
(SQLiteProvider.from_memory_scope -> ProviderRegistry -> ProviderFactory ->
SQLiteStore) bound to this runtime's injected RuntimePaths.memory; it has no
legacy data fallback or migration. Conversation Intelligence composition uses
the completed MS-0025A-D conversation and prompt components only. It does not
compose memory context, reasoning, planning, agents, or execution proposals.
"""

from __future__ import annotations

from jaos.ai import AIManager, ProviderManager
from jaos.ai.bootstrap import initialize_default_provider
from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.intelligence.conversation import (
    ConversationOrchestrator,
    ConversationPolicy,
    ConversationPolicyRegistry,
    ConversationReferenceResolver,
    ConversationSessionManager,
    InMemoryConversationSessionStore,
)
from jaos.intelligence.prompt import (
    IntelligencePromptComposer,
    IntelligencePromptTemplate,
    PromptTemplateRegistry,
)
from jaos.memory.providers.provider_factory import ProviderFactory
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.storage.memory_store import MemoryStore
from jaos.tools.tool_manager import ToolManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.service_metadata import ServiceMetadata

TOOL_MANAGER_SERVICE = "tool_manager_platform"
AI_MANAGER_SERVICE = "ai_manager_platform"
EXECUTIVE_CONTROLLER_SERVICE = "executive_controller_platform"
MEMORY_STORE_SERVICE = "memory_store_platform"
INTELLIGENCE_ORCHESTRATOR_SERVICE = "intelligence_orchestrator_platform"

_CONVERSATION_SYSTEM_INSTRUCTION = (
    "You are the conversational intelligence component of JAOS. "
    "Respond using the supplied conversation context, policy, and resolved "
    "references. Do not claim that tools, actions, approvals, or external "
    "operations occurred unless their results are explicitly provided."
)
_CONVERSATION_TASK_INSTRUCTION = (
    "Produce a helpful response to the user's current message. "
    "Preserve conversational continuity and respect the supplied context and "
    "policy."
)
_INTELLIGENCE_PROMPT_COMPOSER_COMPONENT = "intelligence_prompt_composer"


class CompositionError(RuntimeError):
    """Raised when platform composition is attempted or fails illegitimately."""


class CompositionTeardownError(RuntimeError):
    """Raised when one or more composed platforms failed to tear down cleanly."""


class PlatformComposition:
    """Compose the canonical platforms into one started Runtime authority."""

    def __init__(self, runtime: PlatformRuntime) -> None:
        self.runtime = runtime
        self._service_names: list[str] = []
        self._pending_ai_manager: AIManager | None = None
        self._pending_memory_store: MemoryStore | None = None
        self._prompt_composer: IntelligencePromptComposer | None = None
        self._intelligence_orchestrator: ConversationOrchestrator | None = None

    @property
    def tool_manager(self) -> ToolManager:
        return self.runtime.container.resolve(TOOL_MANAGER_SERVICE)

    @property
    def ai_manager(self) -> AIManager:
        return self.runtime.container.resolve(AI_MANAGER_SERVICE)

    @property
    def executive_controller(self) -> ExecutiveController:
        return self.runtime.container.resolve(EXECUTIVE_CONTROLLER_SERVICE)

    @property
    def memory_store(self) -> MemoryStore:
        return self.runtime.container.resolve(MEMORY_STORE_SERVICE)

    @property
    def intelligence_orchestrator(self) -> ConversationOrchestrator:
        return self.runtime.container.resolve(INTELLIGENCE_ORCHESTRATOR_SERVICE)

    def compose(self) -> None:
        """Construct and register the real platforms.

        Requires the runtime to already be READY, so platform composition
        can never proceed on top of an unready runtime. Rollback-scoped: if
        a later platform fails to construct, every platform already
        registered by this call is unregistered so no live, orphaned
        platform survives a failed composition.
        """

        if self.runtime.lifecycle_state != RuntimeLifecycleState.READY:
            raise CompositionError(
                "PlatformComposition requires the runtime to be READY, got "
                f"{self.runtime.lifecycle_state.value}"
            )

        if (
            self._service_names
            or self._pending_ai_manager is not None
            or self._pending_memory_store is not None
            or self._prompt_composer is not None
            or self._intelligence_orchestrator is not None
        ):
            raise CompositionError("PlatformComposition is already composed")

        try:
            tool_manager = ToolManager()
            load_tools(tool_manager)
            self._register(TOOL_MANAGER_SERVICE, tool_manager)

            ai_manager = self._compose_ai_manager()

            executive_controller = ExecutiveController(
                tool_manager,
                ai_manager=ai_manager,
            )
            self._register(EXECUTIVE_CONTROLLER_SERVICE, executive_controller)

            self._compose_memory_store()
            self._compose_intelligence_orchestrator(ai_manager)
        except Exception as error:
            cleanup_errors, retained_names = self._shutdown_owned_resources()
            cleanup_errors.extend(self._rollback(retained_names))
            self._annotate_cleanup_errors(error, cleanup_errors)
            raise

    def _compose_ai_manager(self) -> AIManager:
        """Initialize and register AI without leaking an orphaned provider."""

        provider_manager = ProviderManager()
        ai_manager = AIManager(provider_manager)
        self._pending_ai_manager = ai_manager
        initialize_default_provider(provider_manager)
        self._register(AI_MANAGER_SERVICE, ai_manager)
        self._pending_ai_manager = None

        return ai_manager

    def _compose_memory_store(self) -> None:
        """Build and register the canonical Memory store.

        Uses the modern provider chain exclusively, bound to injected
        RuntimePaths.memory: no repo-relative path, no legacy data fallback,
        no automatic migration. Registration is folded into this same
        ownership scope so a store that opens successfully but fails to
        register (e.g. a duplicate service name) is still retained until
        compose()'s coordinated resource cleanup closes it successfully.
        """

        provider = SQLiteProvider.from_memory_scope(
            self.runtime.runtime_paths.memory
        )
        registry = ProviderRegistry()
        registry.register(provider)
        store = ProviderFactory(registry).create_default()
        self._pending_memory_store = store
        self._register(MEMORY_STORE_SERVICE, store)
        self._pending_memory_store = None

    def _compose_intelligence_orchestrator(self, ai_manager: AIManager) -> None:
        """Build, initialize, and register canonical Conversation Intelligence."""

        session_store = InMemoryConversationSessionStore()

        policy_registry = ConversationPolicyRegistry()
        policy_registry.register_policy(
            ConversationPolicy(policy_name="default"),
            make_default=True,
        )

        session_manager = ConversationSessionManager(
            session_store,
            policy_registry,
        )
        reference_resolver = ConversationReferenceResolver()

        template_registry = PromptTemplateRegistry()
        template_registry.register_template(
            IntelligencePromptTemplate(
                template_id="conversation",
                version="1.0",
                system_instruction=_CONVERSATION_SYSTEM_INSTRUCTION,
                task_instruction=_CONVERSATION_TASK_INSTRUCTION,
            ),
            make_default=True,
        )

        prompt_composer = IntelligencePromptComposer(template_registry)
        self._prompt_composer = prompt_composer
        prompt_composer.initialize()

        orchestrator = ConversationOrchestrator(
            session_manager,
            policy_registry,
            reference_resolver,
            prompt_composer,
            ai_manager,
            template_id="conversation",
            template_version="1.0",
        )
        self._intelligence_orchestrator = orchestrator
        orchestrator.initialize()

        self._register(
            INTELLIGENCE_ORCHESTRATOR_SERVICE,
            orchestrator,
            owner="Intelligence",
        )

    def teardown(self) -> None:
        """Tear down composed platforms in reverse order.

        Continues past an individual platform's shutdown failure and aggregates
        every failure into one CompositionTeardownError, matching
        PlatformRuntime.stop()'s coordinated-shutdown contract. Conversation
        Intelligence shuts down orchestrator before prompt composer. Tool and
        Executive have no shutdown of their own today.
        """

        errors, retained_names = self._shutdown_owned_resources()
        errors.extend(self._rollback(retained_names))

        if errors:
            raise CompositionTeardownError(
                "; ".join(f"{name}: {exc}" for name, exc in errors)
            )

    def _shutdown_owned_resources(
        self,
    ) -> tuple[list[tuple[str, Exception]], set[str]]:
        """Release resources while retaining failed owners for retry."""

        errors: list[tuple[str, Exception]] = []
        retained_names: set[str] = set()

        if (
            INTELLIGENCE_ORCHESTRATOR_SERVICE not in self._service_names
            and (
                self._intelligence_orchestrator is not None
                or self._prompt_composer is not None
            )
        ):
            intelligence_errors = self._shutdown_intelligence_components(
                self._intelligence_orchestrator,
                self._prompt_composer,
            )
            errors.extend(intelligence_errors)
            if intelligence_errors:
                retained_names.add(INTELLIGENCE_ORCHESTRATOR_SERVICE)
            else:
                self._clear_intelligence_references()

        if self._pending_memory_store is not None:
            try:
                if not self._pending_memory_store.is_closed:
                    self._pending_memory_store.close()
                self._pending_memory_store = None
            except Exception as exc:  # noqa: BLE001
                errors.append((MEMORY_STORE_SERVICE, exc))

        if self._pending_ai_manager is not None:
            try:
                self._pending_ai_manager.shutdown()
                self._pending_ai_manager = None
            except Exception as exc:  # noqa: BLE001
                errors.append((AI_MANAGER_SERVICE, exc))
                retained_names.add(AI_MANAGER_SERVICE)

        for name in reversed(self._service_names):
            if name == INTELLIGENCE_ORCHESTRATOR_SERVICE:
                intelligence_errors = self._shutdown_intelligence_components(
                    self._intelligence_orchestrator,
                    self._prompt_composer,
                )
                errors.extend(intelligence_errors)
                if intelligence_errors:
                    retained_names.add(name)
                else:
                    self._clear_intelligence_references()
            elif name == MEMORY_STORE_SERVICE:
                try:
                    store = self.runtime.container.resolve(name)
                    if not store.is_closed:
                        store.close()
                except Exception as exc:  # noqa: BLE001
                    errors.append((name, exc))
                    retained_names.add(name)
            elif name == AI_MANAGER_SERVICE:
                try:
                    self.runtime.container.resolve(name).shutdown()
                except Exception as exc:  # noqa: BLE001
                    errors.append((name, exc))
                    retained_names.add(name)

        return errors, retained_names

    @staticmethod
    def _shutdown_intelligence_components(
        orchestrator: ConversationOrchestrator | None,
        prompt_composer: IntelligencePromptComposer | None,
    ) -> list[tuple[str, Exception]]:
        """Shut down initialized Intelligence components in dependency order."""

        errors: list[tuple[str, Exception]] = []

        if orchestrator is not None:
            try:
                if orchestrator.is_ready:
                    orchestrator.shutdown()
            except Exception as exc:  # noqa: BLE001
                errors.append((INTELLIGENCE_ORCHESTRATOR_SERVICE, exc))

        if prompt_composer is not None:
            try:
                if prompt_composer.is_ready:
                    prompt_composer.shutdown()
            except Exception as exc:  # noqa: BLE001
                errors.append((_INTELLIGENCE_PROMPT_COMPOSER_COMPONENT, exc))

        return errors

    def _clear_intelligence_references(self) -> None:
        self._intelligence_orchestrator = None
        self._prompt_composer = None

    def _register(
        self,
        name: str,
        instance: object,
        *,
        owner: str = "Platform",
    ) -> None:
        if self.runtime.container.is_registered(name):
            raise ValueError(f"Service '{name}' already registered.")

        if self.runtime.registry.is_registered(name):
            raise ValueError(f"Service '{name}' already exists.")

        try:
            self.runtime.container.register(name, instance)
            self.runtime.registry.register(
                ServiceMetadata(name=name, owner=owner)
            )
        except Exception:
            try:
                if self.runtime.registry.is_registered(name):
                    self.runtime.registry.unregister(name)
            except Exception:  # noqa: BLE001, S110
                pass

            try:
                if self.runtime.container.is_registered(name):
                    self.runtime.container.unregister(name)
            except Exception:  # noqa: BLE001, S110
                pass

            raise

        self._service_names.append(name)

    def _rollback(
        self,
        retained_names: set[str] | None = None,
    ) -> list[tuple[str, Exception]]:
        """Unregister owned services except resources retained for retry."""

        errors: list[tuple[str, Exception]] = []
        retained = retained_names or set()

        for name in reversed(self._service_names):
            if name in retained:
                continue

            try:
                if self.runtime.registry.is_registered(name):
                    self.runtime.registry.unregister(name)
            except Exception as exc:  # noqa: BLE001
                errors.append((f"{name}.registry", exc))

            try:
                if self.runtime.container.is_registered(name):
                    self.runtime.container.unregister(name)
            except Exception as exc:  # noqa: BLE001
                errors.append((f"{name}.container", exc))

        self._service_names = [
            name for name in self._service_names if name in retained
        ]
        if INTELLIGENCE_ORCHESTRATOR_SERVICE not in retained:
            self._clear_intelligence_references()
        return errors

    @staticmethod
    def _annotate_cleanup_errors(
        original_error: Exception,
        cleanup_errors: list[tuple[str, Exception]],
    ) -> None:
        """Preserve the original failure while recording cleanup failures."""

        for name, cleanup_error in cleanup_errors:
            original_error.add_note(
                f"cleanup failure for {name}: {cleanup_error}"
            )
