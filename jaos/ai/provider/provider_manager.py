from time import perf_counter

from jaos.ai.provider.ai_provider import AIProvider
from jaos.ai.provider.health import AIProviderHealth, AIProviderHealthStatus
from jaos.ai.provider.models import AIRequest, AIResponse
from jaos.ai.provider.provider_config import AIProviderConfig
from jaos.ai.provider.provider_registry import ProviderRegistry
from jaos.ai.provider.provider_state import AIProviderState


class ProviderManagerError(Exception):
    """Base error for provider manager failures."""


class ProviderDisabledError(ProviderManagerError):
    """Raised when trying to use a disabled provider."""


class ProviderManager:
    """
    Coordinates provider lifecycle, health, state, and generation.

    The Executive Brain should talk to this manager instead of directly
    talking to provider implementations or the provider registry.
    """

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry or ProviderRegistry()
        self._configs: dict[str, AIProviderConfig] = {}
        self._states: dict[str, AIProviderState] = {}

    def register_provider(
        self,
        provider: AIProvider,
        config: AIProviderConfig,
        *,
        set_default: bool = False,
    ) -> None:
        self._registry.register(config.name, provider, set_default=set_default)
        self._configs[config.name] = config
        self._states[config.name] = AIProviderState(
            name=config.name,
            enabled=config.enabled,
            current_model=config.default_model,
        )

    def unregister_provider(self, name: str) -> AIProvider:
        normalized_name = self._normalize_name(name)

        provider = self._registry.unregister(normalized_name)
        self._configs.pop(normalized_name, None)
        self._states.pop(normalized_name, None)

        return provider

    def initialize_provider(self, name: str) -> None:
        normalized_name = self._normalize_name(name)
        provider = self._registry.get(normalized_name)
        config = self._configs[normalized_name]
        state = self._states[normalized_name]

        if not config.enabled or not state.enabled:
            raise ProviderDisabledError(f"AI provider is disabled: {normalized_name}")

        try:
            state.mark_initializing()
            provider.initialize()
            state.mark_initialized(model=config.default_model)
        except Exception as exc:
            state.mark_failed(exc)
            raise ProviderManagerError(
                f"Failed to initialize AI provider: {normalized_name}"
            ) from exc

    def shutdown_provider(self, name: str) -> None:
        normalized_name = self._normalize_name(name)
        provider = self._registry.get(normalized_name)
        state = self._states[normalized_name]

        try:
            state.mark_shutting_down()
            provider.shutdown()
            state.mark_shutdown()
        except Exception as exc:
            state.mark_failed(exc)
            raise ProviderManagerError(
                f"Failed to shutdown AI provider: {normalized_name}"
            ) from exc

    def initialize_all(self) -> None:
        for name in self.list_provider_names():
            self.initialize_provider(name)

    def shutdown_all(self) -> None:
        for name in self.list_provider_names():
            self.shutdown_provider(name)

    def health_check(self, name: str) -> AIProviderHealth:
        normalized_name = self._normalize_name(name)
        provider = self._registry.get(normalized_name)
        state = self._states[normalized_name]

        try:
            health = provider.health()
            state.mark_health_check(
                healthy=health.status == AIProviderHealthStatus.HEALTHY,
                error=health.message or None,
            )
            return health
        except Exception as exc:
            state.mark_health_check(healthy=False, error=exc)
            raise ProviderManagerError(
                f"Failed to check AI provider health: {normalized_name}"
            ) from exc

    def generate(self, request: AIRequest, provider_name: str | None = None) -> AIResponse:
        if not isinstance(request, AIRequest):
            raise TypeError("ProviderManager.generate expects an AIRequest instance")

        provider, state, config = self._resolve_provider(provider_name)

        if not config.enabled or not state.enabled:
            raise ProviderDisabledError(f"AI provider is disabled: {config.name}")

        start_time = perf_counter()

        try:
            response = provider.generate(request)
            latency = perf_counter() - start_time
            state.record_success(latency_seconds=latency)
            return response
        except Exception as exc:
            state.record_failure(exc)
            raise ProviderManagerError(
                f"AI provider generation failed: {config.name}"
            ) from exc

    def get_provider(self, name: str) -> AIProvider:
        return self._registry.get(name)

    def get_config(self, name: str) -> AIProviderConfig:
        return self._configs[self._normalize_name(name)]

    def get_state(self, name: str) -> AIProviderState:
        return self._states[self._normalize_name(name)]

    def get_default_provider_name(self) -> str:
        return self._registry.get_default_name()

    def set_default_provider(self, name: str) -> None:
        self._registry.set_default(name)

    def list_provider_names(self) -> tuple[str, ...]:
        return self._registry.list_provider_names()

    def count(self) -> int:
        return self._registry.count()

    def _resolve_provider(
        self,
        provider_name: str | None,
    ) -> tuple[AIProvider, AIProviderState, AIProviderConfig]:
        if provider_name is None:
            name = self._registry.get_default_name()
        else:
            name = self._normalize_name(provider_name)

        provider = self._registry.get(name)
        state = self._states[name]
        config = self._configs[name]

        return provider, state, config

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized_name = name.strip().lower()

        if not normalized_name:
            raise ValueError("Provider name cannot be empty")

        return normalized_name