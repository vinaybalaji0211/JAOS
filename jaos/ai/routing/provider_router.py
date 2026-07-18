from jaos.ai.provider import ProviderManager
from jaos.ai.provider.provider_registry import ProviderNotFoundError
from jaos.ai.routing.routing_models import (
    ProviderCandidate,
    RoutingRequest,
    RoutingStrategy,
)


class ProviderRouterError(Exception):
    """Base error for provider router failures."""


class NoAvailableProviderError(ProviderRouterError):
    """Raised when no provider can satisfy a routing request."""


class ProviderRouter:
    """
    Selects which provider should execute an AI request.

    The router never executes providers directly.
    Execution is delegated to ProviderManager.

    Alpha routing pipeline:
    1. Validate request
    2. Collect provider candidates
    3. Filter by explicit provider when requested
    4. Filter by availability and capabilities
    5. Apply routing strategy
    6. Return selected provider name
    """

    def __init__(self, provider_manager: ProviderManager) -> None:
        self._provider_manager = provider_manager

    def resolve_provider(self, request: RoutingRequest) -> str:
        if not isinstance(request, RoutingRequest):
            raise TypeError("ProviderRouter.resolve_provider expects a RoutingRequest")

        candidates = self._collect_candidates(request)

        if request.strategy == RoutingStrategy.EXPLICIT:
            return self._select_explicit_provider(request, candidates)

        available_candidates = self._available_candidates(candidates)

        if not available_candidates:
            raise NoAvailableProviderError(
                "No available AI provider can satisfy request"
            )

        if request.strategy == RoutingStrategy.DEFAULT:
            return self._select_default_provider(available_candidates)

        if request.strategy == RoutingStrategy.LOCAL_FIRST:
            return self._select_local_first_provider(available_candidates)

        if request.strategy == RoutingStrategy.CLOUD_FIRST:
            return self._select_cloud_first_provider(available_candidates)

        raise ValueError(f"Unsupported routing strategy: {request.strategy}")

    def _collect_candidates(
        self,
        request: RoutingRequest,
    ) -> tuple[ProviderCandidate, ...]:
        default_provider_name = self._safe_default_provider_name()
        candidates: list[ProviderCandidate] = []

        for provider_name in self._provider_manager.list_provider_names():
            try:
                config = self._provider_manager.get_config(provider_name)
                state = self._provider_manager.get_state(provider_name)
            except (KeyError, ProviderNotFoundError, ValueError):
                continue

            candidates.append(
                ProviderCandidate(
                    name=provider_name,
                    is_default=provider_name == default_provider_name,
                    is_local=config.is_local(),
                    is_cloud=config.is_cloud(),
                    enabled=config.enabled and state.enabled,
                    supports_required_capabilities=config.supports_all(
                        request.required_capabilities
                    ),
                )
            )

        return tuple(candidates)

    def _select_explicit_provider(
        self,
        request: RoutingRequest,
        candidates: tuple[ProviderCandidate, ...],
    ) -> str:
        if request.provider_name is None:
            raise ValueError("Explicit routing requires a provider name.")

        for candidate in candidates:
            if candidate.name == request.provider_name and candidate.is_available():
                return candidate.name

        raise NoAvailableProviderError(
            f"Explicit provider cannot satisfy request: {request.provider_name}"
        )

    def _available_candidates(
        self,
        candidates: tuple[ProviderCandidate, ...],
    ) -> tuple[ProviderCandidate, ...]:
        return tuple(candidate for candidate in candidates if candidate.is_available())

    def _select_default_provider(
        self,
        candidates: tuple[ProviderCandidate, ...],
    ) -> str:
        for candidate in candidates:
            if candidate.is_default:
                return candidate.name

        return self._select_first_provider(candidates)

    def _select_local_first_provider(
        self,
        candidates: tuple[ProviderCandidate, ...],
    ) -> str:
        for candidate in candidates:
            if candidate.is_local:
                return candidate.name

        return self._select_default_provider(candidates)

    def _select_cloud_first_provider(
        self,
        candidates: tuple[ProviderCandidate, ...],
    ) -> str:
        for candidate in candidates:
            if candidate.is_cloud:
                return candidate.name

        return self._select_default_provider(candidates)

    def _select_first_provider(
        self,
        candidates: tuple[ProviderCandidate, ...],
    ) -> str:
        if not candidates:
            raise NoAvailableProviderError(
                "No available AI provider can satisfy request"
            )

        return candidates[0].name

    def _safe_default_provider_name(self) -> str | None:
        try:
            return self._provider_manager.get_default_provider_name()
        except ProviderNotFoundError:
            return None