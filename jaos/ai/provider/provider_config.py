from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AIProviderType(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"
    HYBRID = "hybrid"
    MOCK = "mock"
    CUSTOM = "custom"


class AIProviderCapability(str, Enum):
    CHAT = "chat"
    STREAMING = "streaming"
    TOOLS = "tools"
    EMBEDDINGS = "embeddings"
    VISION = "vision"


class AIProviderConfigError(ValueError):
    """Raised when AI provider configuration is invalid."""


@dataclass(frozen=True)
class AIProviderConfig:
    """
    Configuration model for an AI provider.

    Capabilities describe what the provider can do.
    This lets the router select only providers that can satisfy a request.
    """

    name: str
    provider_type: AIProviderType = AIProviderType.CUSTOM
    enabled: bool = True
    default_model: str | None = None
    timeout_seconds: float = 30.0
    max_retries: int = 2
    environment: str = "default"
    secret_refs: tuple[str, ...] = ()
    capabilities: tuple[AIProviderCapability, ...] = (
        AIProviderCapability.CHAT,
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized_name = self._normalize_required_text(self.name, "Provider name")
        normalized_environment = self._normalize_required_text(
            self.environment,
            "Provider environment",
        )

        normalized_model = None
        if self.default_model is not None:
            stripped_model = self.default_model.strip()
            normalized_model = stripped_model if stripped_model else None

        if self.timeout_seconds <= 0:
            raise AIProviderConfigError("Provider timeout must be greater than zero")

        if self.max_retries < 0:
            raise AIProviderConfigError("Provider max_retries cannot be negative")

        normalized_secret_refs = tuple(
            self._normalize_required_text(secret_ref, "Secret reference")
            for secret_ref in self.secret_refs
        )

        normalized_capabilities = tuple(
            self._normalize_capability(capability)
            for capability in self.capabilities
        )

        if not normalized_capabilities:
            raise AIProviderConfigError("Provider must declare at least one capability")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "environment", normalized_environment)
        object.__setattr__(self, "default_model", normalized_model)
        object.__setattr__(self, "secret_refs", normalized_secret_refs)
        object.__setattr__(self, "capabilities", normalized_capabilities)
        object.__setattr__(self, "metadata", dict(self.metadata))

    def is_local(self) -> bool:
        return self.provider_type in {
            AIProviderType.LOCAL,
            AIProviderType.MOCK,
        }

    def is_cloud(self) -> bool:
        return self.provider_type == AIProviderType.CLOUD

    def requires_secrets(self) -> bool:
        return len(self.secret_refs) > 0

    def supports(self, capability: AIProviderCapability | str) -> bool:
        normalized_capability = self._normalize_capability(capability)
        return normalized_capability in self.capabilities

    def supports_all(self, capabilities: tuple[AIProviderCapability | str, ...]) -> bool:
        return all(self.supports(capability) for capability in capabilities)

    @staticmethod
    def _normalize_required_text(value: str, field_name: str) -> str:
        normalized_value = value.strip().lower()

        if not normalized_value:
            raise AIProviderConfigError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _normalize_capability(
        capability: AIProviderCapability | str,
    ) -> AIProviderCapability:
        if isinstance(capability, AIProviderCapability):
            return capability

        try:
            return AIProviderCapability(capability.strip().lower())
        except ValueError as exc:
            raise AIProviderConfigError(
                f"Unsupported provider capability: {capability}"
            ) from exc