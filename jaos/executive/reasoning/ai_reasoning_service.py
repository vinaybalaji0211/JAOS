from jaos.executive.ai import ExecutiveAIGateway, ExecutiveAIRequest
from jaos.executive.models import ExecutiveResponse


class AIReasoningService:
    """
    Bridges the Executive Platform to the AI Platform through ExecutiveAIGateway.

    The Executive uses this service for reasoning-only fallback.
    The AI Platform does not execute tools directly.
    """

    def __init__(self, gateway: ExecutiveAIGateway) -> None:
        self.gateway = gateway

    def reason(self, user_input: str) -> ExecutiveResponse:
        if not user_input.strip():
            return ExecutiveResponse(
                success=False,
                message="AI reasoning request cannot be empty.",
            )

        response = self.gateway.ask(
            ExecutiveAIRequest(
                goal=user_input,
                metadata={"reasoning_mode": "fallback"},
            )
        )

        return ExecutiveResponse(
            success=True,
            message=response.text,
            output={
                "provider": response.provider,
                "model": response.model,
            },
        )