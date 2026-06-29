"""
JAOS AI Provider Interface

Phase 3 — JAOS-M-0023

Defines the abstract interface that every AI provider
must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from executive_brain.ai.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


class AIProviderInterface(ABC):
    """
    Base interface for all AI providers.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Returns the provider name.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Generate a response from the AI provider.
        """
        raise NotImplementedError

    @abstractmethod
    def health(self) -> AIProviderStatus:
        """
        Returns the current health status of the provider.
        """
        raise NotImplementedError