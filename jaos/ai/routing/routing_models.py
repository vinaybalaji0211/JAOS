from dataclasses import dataclass, field
from enum import Enum


class RoutingStrategy(str, Enum):
    DEFAULT = "default"
    LOCAL_FIRST = "local_first"
    CLOUD_FIRST = "cloud_first"
    EXPLICIT = "explicit"


@dataclass(frozen=True)
class RoutingRequest:
    """
    Describes how an AI provider should be selected.
    """

    provider_name: str | None = None
    strategy: RoutingStrategy = RoutingStrategy.DEFAULT
    required_capabilities: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.provider_name is not None:
            provider_name = self.provider_name.strip().lower()
            object.__setattr__(self, "provider_name", provider_name or None)

        capabilities = tuple(
            capability.strip().lower()
            for capability in self.required_capabilities
            if capability.strip()
        )
        object.__setattr__(self, "required_capabilities", capabilities)


@dataclass(frozen=True)
class ProviderCandidate:
    """
    Internal routing candidate.

    The router uses this lightweight model to separate candidate collection
    from provider selection. It keeps routing logic readable as strategies grow.
    """

    name: str
    is_default: bool
    is_local: bool
    is_cloud: bool
    enabled: bool
    supports_required_capabilities: bool

    def is_available(self) -> bool:
        return self.enabled and self.supports_required_capabilities