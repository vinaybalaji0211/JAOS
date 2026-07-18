from dataclasses import dataclass, field
from typing import Any

from jaos.ai import AIGenerateRequest, AIManager, ParsedResponse


@dataclass(frozen=True)
class ExecutiveAIRequest:
    """
    Request model used by the Executive Platform to ask the AI Platform
    for assistance.

    The Executive does not send provider-specific requests directly.
    """

    goal: str
    context: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        goal = self.goal.strip()

        if not goal:
            raise ValueError("Executive AI request goal cannot be empty")

        object.__setattr__(self, "goal", goal)

        if self.context is not None:
            context = self.context.strip()
            object.__setattr__(self, "context", context or None)

        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class ExecutiveAIResponse:
    """
    Response model returned from AI Platform to Executive Platform.
    """

    text: str
    provider: str
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        text = self.text.strip()
        provider = self.provider.strip().lower()

        if not text:
            raise ValueError("Executive AI response text cannot be empty")

        if not provider:
            raise ValueError("Executive AI response provider cannot be empty")

        object.__setattr__(self, "text", text)
        object.__setattr__(self, "provider", provider)

        if self.model is not None:
            model = self.model.strip()
            object.__setattr__(self, "model", model or None)

        object.__setattr__(self, "metadata", dict(self.metadata or {}))


class ExecutiveAIGateway:
    """
    Boundary between the Executive Platform and the AI Platform.

    The Executive Platform must use this gateway instead of directly
    depending on provider internals or AI Platform subcomponents.
    """

    def __init__(self, ai_manager: AIManager) -> None:
        self._ai_manager = ai_manager

    def ask(self, request: ExecutiveAIRequest) -> ExecutiveAIResponse:
        if not isinstance(request, ExecutiveAIRequest):
            raise TypeError("ExecutiveAIGateway.ask expects an ExecutiveAIRequest")

        prompt = self._build_prompt(request)

        parsed_response = self._ai_manager.generate_from_request(
            AIGenerateRequest(
                prompt=prompt,
                metadata={
                    **request.metadata,
                    "source": "executive",
                },
            )
        )

        return self._to_executive_response(parsed_response)

    @staticmethod
    def _build_prompt(request: ExecutiveAIRequest) -> str:
        if request.context is None:
            return request.goal

        return (
            "Goal:\n"
            f"{request.goal}\n\n"
            "Context:\n"
            f"{request.context}"
        )

    @staticmethod
    def _to_executive_response(
        parsed_response: ParsedResponse,
    ) -> ExecutiveAIResponse:
        return ExecutiveAIResponse(
            text=parsed_response.text,
            provider=parsed_response.metadata.provider,
            model=parsed_response.metadata.model,
            metadata={
                "finish_reason": parsed_response.metadata.finish_reason.value,
                "source_metadata": parsed_response.metadata.source_metadata,
            },
        )