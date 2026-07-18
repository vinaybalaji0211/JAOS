from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AIRequest:
    """
    Standard request passed into every AI provider.

    This model keeps provider calls consistent across local, cloud,
    mock, and future multi-modal providers. The prompt is required
    because an empty request cannot produce a meaningful AI response.
    """

    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    temperature: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        prompt = self.prompt.strip()

        if not prompt:
            raise ValueError("AI request prompt cannot be empty")

        object.__setattr__(self, "prompt", prompt)

        if self.model is not None:
            model = self.model.strip()
            object.__setattr__(self, "model", model or None)

        if self.system_prompt is not None:
            system_prompt = self.system_prompt.strip()
            object.__setattr__(self, "system_prompt", system_prompt or None)

        if self.temperature < 0:
            raise ValueError("AI request temperature cannot be negative")

        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class AIResponse:
    """
    Standard response returned by every AI provider.

    Provider is required so response parsing, routing analytics,
    telemetry, and debugging can always trace where a response came from.
    """

    text: str
    provider: str
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        text = self.text.strip()
        provider = self.provider.strip().lower()

        if not text:
            raise ValueError("AI response text cannot be empty")

        if not provider:
            raise ValueError("AI response provider cannot be empty")

        object.__setattr__(self, "text", text)
        object.__setattr__(self, "provider", provider)

        if self.model is not None:
            model = self.model.strip()
            object.__setattr__(self, "model", model or None)

        object.__setattr__(self, "metadata", dict(self.metadata or {}))