"""
JAOS Prompt Engine

Phase 3 — JAOS-M-0025

Validates and formats prompt messages into provider-ready prompts.
"""

from __future__ import annotations

from executive_brain.ai.prompt.prompt_models import (
    PromptMessage,
    PromptRequest,
    PromptResponse,
    PromptRole,
)
from executive_brain.ai.providers.ai_provider_models import AIProviderRequest


class PromptEngine:
    """
    Builds provider-independent prompts from structured messages.
    """

    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        self._validate_request(request)

        sections: list[str] = []

        for message in request.messages:
            role_label = self._format_role(message.role)
            sections.append(f"{role_label}:\n{message.content.strip()}")

        return PromptResponse(
            prompt="\n\n".join(sections),
            message_count=len(request.messages),
        )

    def to_provider_request(
        self,
        request: PromptRequest,
    ) -> AIProviderRequest:
        response = self.build_prompt(request)

        return AIProviderRequest(
            prompt=response.prompt,
            parameters={"message_count": response.message_count},
        )

    def _validate_request(self, request: PromptRequest) -> None:
        if not isinstance(request, PromptRequest):
            raise TypeError("request must be a PromptRequest")

        if not request.messages:
            raise ValueError("prompt request must contain at least one message")

        for message in request.messages:
            self._validate_message(message)

    def _validate_message(self, message: PromptMessage) -> None:
        if not isinstance(message, PromptMessage):
            raise TypeError("message must be a PromptMessage")

        if not isinstance(message.role, PromptRole):
            raise ValueError("message role must be a PromptRole")

        if not isinstance(message.content, str):
            raise TypeError("message content must be a string")

        if not message.content.strip():
            raise ValueError("message content cannot be empty")

    def _format_role(self, role: PromptRole) -> str:
        return role.value.upper()