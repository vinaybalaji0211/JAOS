from dataclasses import dataclass, field
from typing import Any

from jaos.ai.routing import RoutingStrategy


@dataclass(frozen=True)
class AIGenerateRequest:
    """
    High-level request accepted by the AI Platform.

    This model is intentionally above provider-level AIRequest.
    It represents what JAOS wants from the AI Platform, not what
    a specific provider needs.
    """

    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    routing_strategy: RoutingStrategy = RoutingStrategy.DEFAULT
    provider_name: str | None = None
    temperature: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        prompt = self.prompt.strip()

        if not prompt:
            raise ValueError("AI generate request prompt cannot be empty")

        object.__setattr__(self, "prompt", prompt)

        if self.model is not None:
            model = self.model.strip()
            object.__setattr__(self, "model", model or None)

        if self.system_prompt is not None:
            system_prompt = self.system_prompt.strip()
            object.__setattr__(self, "system_prompt", system_prompt or None)

        if self.provider_name is not None:
            provider_name = self.provider_name.strip().lower()
            object.__setattr__(self, "provider_name", provider_name or None)

        if self.temperature < 0:
            raise ValueError("AI generate request temperature cannot be negative")

        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class AIPlatformStatus:
    """
    Lightweight status model for the AI Platform Manager.
    """

    provider_count: int
    default_provider: str | None
    context_items: int
    conversation_turns: int

    def __post_init__(self) -> None:
        if self.provider_count < 0:
            raise ValueError("Provider count cannot be negative")

        if self.context_items < 0:
            raise ValueError("Context item count cannot be negative")

        if self.conversation_turns < 0:
            raise ValueError("Conversation turn count cannot be negative")

        if self.default_provider is not None:
            default_provider = self.default_provider.strip().lower()
            object.__setattr__(
                self,
                "default_provider",
                default_provider or None,
            )