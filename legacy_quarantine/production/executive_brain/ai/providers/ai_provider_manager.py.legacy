"""
JAOS AI Provider Manager

Phase 3 — JAOS-M-0024

Manages registered AI providers and routes requests to the selected provider.
"""

from __future__ import annotations

from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
)


class AIProviderManager:
    """
    Registry and dispatcher for AI providers.
    """

    def __init__(self) -> None:
        self._providers: dict[str, AIProviderInterface] = {}
        self._default_provider_name: str | None = None

    def register_provider(self, provider: AIProviderInterface) -> None:
        if not isinstance(provider, AIProviderInterface):
            raise TypeError("provider must implement AIProviderInterface")

        provider_name = provider.provider_name

        if not provider_name:
            raise ValueError("provider name cannot be empty")

        if provider_name in self._providers:
            raise ValueError(f"provider already registered: {provider_name}")

        self._providers[provider_name] = provider

        if self._default_provider_name is None:
            self._default_provider_name = provider_name

    def unregister_provider(self, provider_name: str) -> None:
        if provider_name not in self._providers:
            raise KeyError(f"provider not found: {provider_name}")

        del self._providers[provider_name]

        if self._default_provider_name == provider_name:
            self._default_provider_name = next(iter(self._providers), None)

    def get_provider(self, provider_name: str) -> AIProviderInterface:
        if provider_name not in self._providers:
            raise KeyError(f"provider not found: {provider_name}")

        return self._providers[provider_name]

    def list_providers(self) -> list[str]:
        return list(self._providers.keys())

    def has_provider(self, provider_name: str) -> bool:
        return provider_name in self._providers

    def set_default_provider(self, provider_name: str) -> None:
        if provider_name not in self._providers:
            raise KeyError(f"provider not found: {provider_name}")

        self._default_provider_name = provider_name

    def get_default_provider(self) -> AIProviderInterface:
        if self._default_provider_name is None:
            raise RuntimeError("no default provider configured")

        return self.get_provider(self._default_provider_name)

    def generate(
        self,
        request: AIProviderRequest,
        provider_name: str | None = None,
    ) -> AIProviderResponse:
        provider = (
            self.get_provider(provider_name)
            if provider_name is not None
            else self.get_default_provider()
        )

        return provider.generate(request)