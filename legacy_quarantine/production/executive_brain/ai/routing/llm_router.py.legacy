"""
JAOS LLM Router

Phase 3 — JAOS-M-0028

Routes AI requests through the AI Provider Manager.
"""

from __future__ import annotations

from executive_brain.ai.providers.ai_provider_manager import AIProviderManager
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
)


class LLMRouter:
    """
    Routes AIProviderRequest objects to registered AI providers.

    Alpha scope:
    - Default provider routing
    - Manual provider selection
    """

    def __init__(self, provider_manager: AIProviderManager) -> None:
        if not isinstance(provider_manager, AIProviderManager):
            raise TypeError("provider_manager must be an AIProviderManager")

        self._provider_manager = provider_manager

    def route(
        self,
        request: AIProviderRequest,
        provider_name: str | None = None,
    ) -> AIProviderResponse:
        if not isinstance(request, AIProviderRequest):
            raise TypeError("request must be an AIProviderRequest")

        if provider_name is not None and not provider_name.strip():
            raise ValueError("provider_name cannot be empty")

        return self._provider_manager.generate(
            request=request,
            provider_name=provider_name,
        )