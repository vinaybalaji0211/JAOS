from jaos.ai.ai_models import AIGenerateRequest, AIPlatformStatus
from jaos.ai.composition import AIPlatformComposition
from jaos.ai.context import ContextManager
from jaos.ai.diagnostics import AIStatusProvider, DiagnosticStatus
from jaos.ai.identity import IdentityManager, SystemPromptBuilder
from jaos.ai.prompt import PromptManager
from jaos.ai.provider import AIRequest, ProviderManager
from jaos.ai.response import ParsedResponse, ResponseManager
from jaos.ai.routing import ProviderRouter, RoutingRequest
from jaos.ai.telemetry import AIMetrics


class AIManager:
    """
    Single public orchestration entry point for the AI Platform.

    AIManager coordinates the full AI request lifecycle while delegating
    internal dependency wiring to AIPlatformComposition.
    """

    def __init__(
        self,
        provider_manager: ProviderManager,
        *,
        context_manager: ContextManager | None = None,
        prompt_manager: PromptManager | None = None,
        provider_router: ProviderRouter | None = None,
        response_manager: ResponseManager | None = None,
        metrics: AIMetrics | None = None,
        identity_manager: IdentityManager | None = None,
        system_prompt_builder: SystemPromptBuilder | None = None,
    ) -> None:
        self._composition = AIPlatformComposition(
            provider_manager=provider_manager,
            context_manager=context_manager or ContextManager(),
            prompt_manager=prompt_manager or PromptManager(),
            provider_router=provider_router or ProviderRouter(provider_manager),
            response_manager=response_manager or ResponseManager(),
        )
        self._metrics = metrics or AIMetrics()
        self._identity_manager = identity_manager or IdentityManager()
        self._system_prompt_builder = system_prompt_builder or SystemPromptBuilder()
        self._status_provider = AIStatusProvider(provider_manager)

    def generate(self, prompt: str, **kwargs: object) -> ParsedResponse:
        request = AIGenerateRequest(prompt=prompt, **kwargs)
        return self.generate_from_request(request)

    def generate_from_request(self, request: AIGenerateRequest) -> ParsedResponse:
        if not isinstance(request, AIGenerateRequest):
            raise TypeError(
                "AIManager.generate_from_request expects an AIGenerateRequest instance"
            )

        provider_name: str | None = None

        try:
            identity = self._identity_manager.get_identity()
            jaos_system_prompt = self._system_prompt_builder.build(identity)

            system_prompt = (
                request.system_prompt
                if request.system_prompt is not None
                else jaos_system_prompt
            )

            prompt_sections = self._composition.context_manager.build_prompt_sections()

            final_prompt = self._composition.prompt_manager.build_prompt(
                user_prompt=request.prompt,
                sections=prompt_sections,
            )

            provider_name = self._composition.provider_router.resolve_provider(
                RoutingRequest(
                    strategy=request.routing_strategy,
                    provider_name=request.provider_name,
                )
            )

            provider_response = self._composition.provider_manager.generate(
                AIRequest(
                    prompt=final_prompt,
                    model=request.model,
                    system_prompt=system_prompt,
                    temperature=request.temperature,
                    metadata={
                        **request.metadata,
                        "jaos_identity_version": identity.version,
                    },
                ),
                provider_name=provider_name,
            )

            self._metrics.record_success(
                provider=provider_response.provider,
                model=provider_response.model,
            )

            return self._composition.response_manager.process(provider_response)

        except Exception:
            self._metrics.record_failure(
                provider=provider_name,
                model=request.model,
            )
            raise

    def get_context_manager(self) -> ContextManager:
        return self._composition.context_manager

    def get_prompt_manager(self) -> PromptManager:
        return self._composition.prompt_manager

    def get_provider_manager(self) -> ProviderManager:
        return self._composition.provider_manager

    def get_provider_router(self) -> ProviderRouter:
        return self._composition.provider_router

    def get_response_manager(self) -> ResponseManager:
        return self._composition.response_manager

    def get_identity_manager(self) -> IdentityManager:
        return self._identity_manager

    def get_metrics(self) -> AIMetrics:
        return self._metrics

    def get_diagnostic_status(self) -> DiagnosticStatus:
        return self._status_provider.get_status()

    def get_system_prompt(self) -> str:
        identity = self._identity_manager.get_identity()
        return self._system_prompt_builder.build(identity)

    def get_status(self) -> AIPlatformStatus:
        try:
            default_provider = (
                self._composition.provider_manager.get_default_provider_name()
            )
        except Exception:
            default_provider = None

        return AIPlatformStatus(
            provider_count=self._composition.provider_manager.count(),
            default_provider=default_provider,
            context_items=len(self._composition.context_manager.list_context()),
            conversation_turns=len(
                self._composition.context_manager.list_conversation()
            ),
        )