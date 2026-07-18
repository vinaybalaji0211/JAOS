"""
JAOS Memory Platform

Memory Provider Factory

Creates MemoryStore instances through registered memory providers.
"""

from __future__ import annotations

from collections.abc import Iterable

from jaos.memory.providers.memory_provider import MemoryProvider
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.storage.memory_store import MemoryStore


class ProviderFactory:
    """
    Create memory stores through a ProviderRegistry.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:
        """
        Initialize the provider factory.

        Args:
            registry:
                Registry used to resolve memory providers.
        """
        if not isinstance(registry, ProviderRegistry):
            raise TypeError(
                "registry must be a ProviderRegistry"
            )

        self._registry = registry

    @property
    def registry(self) -> ProviderRegistry:
        """
        Return the provider registry used by this factory.
        """
        return self._registry

    def create(
        self,
        provider_id: str | None = None,
        *,
        required_capabilities: Iterable[
            ProviderCapability
        ] = (),
        require_healthy: bool = True,
    ) -> MemoryStore:
        """
        Create a MemoryStore from a registered provider.

        When provider_id is None, the registry's default provider
        is used.
        """
        required = self._normalize_capabilities(
            required_capabilities
        )

        provider = self.resolve_provider(provider_id)

        provider.capabilities.require_all(required)

        if require_healthy and not provider.health_check():
            raise RuntimeError(
                "Memory provider health check failed: "
                f"{provider.provider_id}"
            )

        store = provider.create_store()

        if not isinstance(store, MemoryStore):
            raise RuntimeError(
                "Memory provider returned an invalid store: "
                f"{provider.provider_id}"
            )

        return store

    def create_default(
        self,
        *,
        required_capabilities: Iterable[
            ProviderCapability
        ] = (),
        require_healthy: bool = True,
    ) -> MemoryStore:
        """
        Create a store using the registry's default provider.
        """
        return self.create(
            required_capabilities=required_capabilities,
            require_healthy=require_healthy,
        )

    def resolve_provider(
        self,
        provider_id: str | None = None,
    ) -> MemoryProvider:
        """
        Resolve a requested provider or the default provider.
        """
        if provider_id is None:
            return self._registry.get_default()

        if not isinstance(provider_id, str):
            raise TypeError(
                "provider_id must be a string or None"
            )

        if not provider_id.strip():
            raise ValueError(
                "provider_id must not be empty"
            )

        return self._registry.get(provider_id)

    def supports(
        self,
        capability: ProviderCapability,
        *,
        provider_id: str | None = None,
    ) -> bool:
        """
        Return whether a resolved provider supports a capability.
        """
        if not isinstance(capability, ProviderCapability):
            raise TypeError(
                "capability must be a ProviderCapability"
            )

        provider = self.resolve_provider(provider_id)

        return provider.supports(capability)

    def available_provider_ids(self) -> tuple[str, ...]:
        """
        Return all registered provider IDs.
        """
        return self._registry.provider_ids()

    @staticmethod
    def _normalize_capabilities(
        capabilities: Iterable[ProviderCapability],
    ) -> tuple[ProviderCapability, ...]:
        """
        Validate and normalize required capabilities.
        """
        if isinstance(capabilities, str):
            raise TypeError(
                "required_capabilities must contain "
                "ProviderCapability values"
            )

        try:
            normalized = tuple(capabilities)
        except TypeError as exc:
            raise TypeError(
                "required_capabilities must be an iterable of "
                "ProviderCapability values"
            ) from exc

        for capability in normalized:
            if not isinstance(
                capability,
                ProviderCapability,
            ):
                raise TypeError(
                    "required_capabilities must contain "
                    "ProviderCapability values"
                )

        return normalized