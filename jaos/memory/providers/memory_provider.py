"""
JAOS Memory Platform

Memory Provider Contract

Defines the abstract interface implemented by every
memory provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.providers.provider_capabilities import (
    ProviderCapabilities,
)
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)
from jaos.memory.providers.provider_descriptor import (
    ProviderDescriptor,
)
from jaos.memory.storage.memory_store import MemoryStore


class MemoryProvider(ABC):
    """
    Base class for every memory provider.
    """

    @property
    @abstractmethod
    def descriptor(self) -> ProviderDescriptor:
        """
        Return provider metadata.
        """

    @property
    def provider_id(self) -> str:
        """
        Return the provider's unique identifier.
        """
        return self.descriptor.provider_id

    @property
    def provider_name(self) -> str:
        """
        Return the human-readable provider name.
        """
        return self.descriptor.provider_name

    @property
    def provider_version(self) -> str:
        """
        Return the provider implementation version.
        """
        return self.descriptor.provider_version

    @property
    def capabilities(self) -> ProviderCapabilities:
        """
        Return the capabilities advertised by the provider.
        """
        return self.descriptor.capabilities

    def supports(
        self,
        capability: ProviderCapability,
    ) -> bool:
        """
        Return whether the provider supports a capability.
        """
        return self.capabilities.supports(capability)

    @abstractmethod
    def create_store(self) -> MemoryStore:
        """
        Create a new MemoryStore instance.
        """

    def initialize(self) -> None:
        """
        Perform optional provider-level initialization.
        """

    def shutdown(self) -> None:
        """
        Perform optional provider-level shutdown.
        """

    def health_check(self) -> bool:
        """
        Return whether the provider is healthy and available.
        """
        return True

    def __repr__(self) -> str:
        """
        Return a developer-friendly provider representation.
        """
        return (
            f"{self.__class__.__name__}"
            f"(provider_id={self.provider_id!r})"
        )