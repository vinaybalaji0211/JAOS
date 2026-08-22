"""
JAOS Memory Platform

Memory Provider Registry

Stores and resolves registered memory providers.
"""

from __future__ import annotations

from collections.abc import Iterator
from threading import RLock

from jaos.memory.providers.memory_provider import MemoryProvider
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)


class ProviderRegistry:
    """
    Thread-safe registry of available memory providers.
    """

    def __init__(self) -> None:
        """
        Initialize an empty provider registry.
        """
        self._providers: dict[str, MemoryProvider] = {}
        self._default_provider_id: str | None = None
        self._lock = RLock()

    @property
    def default_provider_id(self) -> str | None:
        """
        Return the currently configured default provider ID.
        """
        with self._lock:
            return self._default_provider_id

    def register(
        self,
        provider: MemoryProvider,
        *,
        make_default: bool = False,
        replace: bool = False,
    ) -> None:
        """
        Register a memory provider.

        Args:
            provider:
                Provider instance to register.
            make_default:
                Whether this provider should become the default.
            replace:
                Whether an existing provider with the same ID may
                be replaced.
        """
        self._validate_provider(provider)

        provider_id = provider.provider_id

        with self._lock:
            if provider_id in self._providers and not replace:
                raise ValueError(
                    "Memory provider is already registered: "
                    f"{provider_id}"
                )

            previous = self._providers.get(provider_id)

            if previous is not None and previous is not provider:
                previous.shutdown()

            provider.initialize()
            self._providers[provider_id] = provider

            if (
                make_default
                or self._default_provider_id is None
                or provider.descriptor.is_default
            ):
                self._default_provider_id = provider_id

    def unregister(
        self,
        provider_id: str,
    ) -> MemoryProvider | None:
        """
        Remove and return a registered provider.

        Returns None when the provider is not registered.
        """
        normalized_id = self._normalize_provider_id(provider_id)

        with self._lock:
            provider = self._providers.pop(
                normalized_id,
                None,
            )

            if provider is None:
                return None

            provider.shutdown()

            if self._default_provider_id == normalized_id:
                self._default_provider_id = self._select_next_default_id()

            return provider

    def get(
        self,
        provider_id: str,
    ) -> MemoryProvider:
        """
        Return a registered provider.

        Raises:
            KeyError:
                If the provider is not registered.
        """
        normalized_id = self._normalize_provider_id(provider_id)

        with self._lock:
            provider = self._providers.get(normalized_id)

            if provider is None:
                raise KeyError(
                    "Memory provider is not registered: "
                    f"{normalized_id}"
                )

            return provider

    def get_optional(
        self,
        provider_id: str,
    ) -> MemoryProvider | None:
        """
        Return a registered provider or None.
        """
        normalized_id = self._normalize_provider_id(provider_id)

        with self._lock:
            return self._providers.get(normalized_id)

    def get_default(self) -> MemoryProvider:
        """
        Return the default provider.

        Raises:
            RuntimeError:
                If no default provider is available.
        """
        with self._lock:
            if self._default_provider_id is None:
                raise RuntimeError(
                    "No default memory provider is registered"
                )

            provider = self._providers.get(
                self._default_provider_id
            )

            if provider is None:
                raise RuntimeError(
                    "Default memory provider is unavailable: "
                    f"{self._default_provider_id}"
                )

            return provider

    def set_default(
        self,
        provider_id: str,
    ) -> None:
        """
        Select a registered provider as the default.
        """
        normalized_id = self._normalize_provider_id(provider_id)

        with self._lock:
            if normalized_id not in self._providers:
                raise KeyError(
                    "Memory provider is not registered: "
                    f"{normalized_id}"
                )

            self._default_provider_id = normalized_id

    def contains(
        self,
        provider_id: str,
    ) -> bool:
        """
        Return whether a provider is registered.
        """
        normalized_id = self._normalize_provider_id(provider_id)

        with self._lock:
            return normalized_id in self._providers

    def find_supporting(
        self,
        capability: ProviderCapability,
    ) -> tuple[MemoryProvider, ...]:
        """
        Return providers supporting one capability.
        """
        self._validate_capability(capability)

        with self._lock:
            matches = [
                provider
                for provider in self._providers.values()
                if provider.supports(capability)
            ]

        return tuple(
            sorted(
                matches,
                key=lambda provider: provider.provider_id,
            )
        )

    def find_supporting_all(
        self,
        capabilities: tuple[ProviderCapability, ...],
    ) -> tuple[MemoryProvider, ...]:
        """
        Return providers supporting all requested capabilities.
        """
        if not isinstance(capabilities, tuple):
            raise TypeError(
                "capabilities must be a tuple of "
                "ProviderCapability values"
            )

        for capability in capabilities:
            self._validate_capability(capability)

        with self._lock:
            matches = [
                provider
                for provider in self._providers.values()
                if provider.capabilities.supports_all(capabilities)
            ]

        return tuple(
            sorted(
                matches,
                key=lambda provider: provider.provider_id,
            )
        )

    def list_providers(self) -> tuple[MemoryProvider, ...]:
        """
        Return all registered providers in deterministic order.
        """
        with self._lock:
            providers = tuple(self._providers.values())

        return tuple(
            sorted(
                providers,
                key=lambda provider: provider.provider_id,
            )
        )

    def provider_ids(self) -> tuple[str, ...]:
        """
        Return registered provider IDs in deterministic order.
        """
        with self._lock:
            return tuple(sorted(self._providers))

    def clear(self) -> int:
        """
        Shut down and remove all providers.

        Every provider is given a chance to shut down even if another
        provider's shutdown fails; failures are aggregated and raised
        together after every provider has been attempted.

        Returns:
            Number of providers removed.
        """
        with self._lock:
            providers = tuple(self._providers.values())
            removed_count = len(providers)

            self._providers.clear()
            self._default_provider_id = None

        errors: list[tuple[str, Exception]] = []

        for provider in providers:
            try:
                provider.shutdown()
            except Exception as exc:
                errors.append((provider.provider_id, exc))

        if errors:
            raise RuntimeError(
                "Failed to shut down memory providers: "
                + "; ".join(
                    f"{provider_id}: {exc}"
                    for provider_id, exc in errors
                )
            )

        return removed_count

    def healthy_providers(self) -> tuple[MemoryProvider, ...]:
        """
        Return providers whose health checks pass.
        """
        with self._lock:
            providers = tuple(self._providers.values())

        healthy = [
            provider
            for provider in providers
            if provider.health_check()
        ]

        return tuple(
            sorted(
                healthy,
                key=lambda provider: provider.provider_id,
            )
        )

    def __contains__(
        self,
        provider_id: object,
    ) -> bool:
        """
        Support membership checks using provider IDs.
        """
        if not isinstance(provider_id, str):
            return False

        try:
            return self.contains(provider_id)
        except ValueError:
            return False

    def __iter__(self) -> Iterator[MemoryProvider]:
        """
        Iterate over providers in deterministic order.
        """
        return iter(self.list_providers())

    def __len__(self) -> int:
        """
        Return the number of registered providers.
        """
        with self._lock:
            return len(self._providers)

    def __bool__(self) -> bool:
        """
        Return whether any provider is registered.
        """
        return len(self) > 0

    def _select_next_default_id(self) -> str | None:
        """
        Select the next deterministic default provider.
        """
        if not self._providers:
            return None

        return sorted(self._providers)[0]

    @staticmethod
    def _normalize_provider_id(
        provider_id: str,
    ) -> str:
        """
        Validate and normalize a provider ID.
        """
        if not isinstance(provider_id, str):
            raise TypeError(
                "provider_id must be a string"
            )

        normalized_id = provider_id.strip()

        if not normalized_id:
            raise ValueError(
                "provider_id must not be empty"
            )

        return normalized_id

    @staticmethod
    def _validate_provider(
        provider: MemoryProvider,
    ) -> None:
        """
        Validate a memory provider instance.
        """
        if not isinstance(provider, MemoryProvider):
            raise TypeError(
                "provider must be a MemoryProvider"
            )

    @staticmethod
    def _validate_capability(
        capability: ProviderCapability,
    ) -> None:
        """
        Validate one provider capability.
        """
        if not isinstance(capability, ProviderCapability):
            raise TypeError(
                "capability must be a ProviderCapability"
            )