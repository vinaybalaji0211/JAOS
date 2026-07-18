from threading import RLock

from jaos.ai.provider.ai_provider import AIProvider


class ProviderRegistryError(Exception):
    """Base error for provider registry failures."""


class ProviderAlreadyRegisteredError(ProviderRegistryError):
    """Raised when a provider name is already registered."""


class ProviderNotFoundError(ProviderRegistryError):
    """Raised when a provider cannot be found."""


class ProviderRegistry:
    """
    Thread-safe registry for AI providers.

    This registry does not initialize or shut down providers.
    It only stores and retrieves provider instances.
    """

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}
        self._default_provider_name: str | None = None
        self._lock = RLock()

    def register(self, name: str, provider: AIProvider, *, set_default: bool = False) -> None:
        normalized_name = self._normalize_name(name)

        with self._lock:
            if normalized_name in self._providers:
                raise ProviderAlreadyRegisteredError(
                    f"AI provider already registered: {normalized_name}"
                )

            self._providers[normalized_name] = provider

            if set_default or self._default_provider_name is None:
                self._default_provider_name = normalized_name

    def unregister(self, name: str) -> AIProvider:
        normalized_name = self._normalize_name(name)

        with self._lock:
            if normalized_name not in self._providers:
                raise ProviderNotFoundError(f"AI provider not found: {normalized_name}")

            provider = self._providers.pop(normalized_name)

            if self._default_provider_name == normalized_name:
                self._default_provider_name = next(iter(self._providers), None)

            return provider

    def get(self, name: str) -> AIProvider:
        normalized_name = self._normalize_name(name)

        with self._lock:
            if normalized_name not in self._providers:
                raise ProviderNotFoundError(f"AI provider not found: {normalized_name}")

            return self._providers[normalized_name]

    def has(self, name: str) -> bool:
        normalized_name = self._normalize_name(name)

        with self._lock:
            return normalized_name in self._providers

    def list_provider_names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._providers.keys()))

    def count(self) -> int:
        with self._lock:
            return len(self._providers)

    def clear(self) -> None:
        with self._lock:
            self._providers.clear()
            self._default_provider_name = None

    def set_default(self, name: str) -> None:
        normalized_name = self._normalize_name(name)

        with self._lock:
            if normalized_name not in self._providers:
                raise ProviderNotFoundError(f"AI provider not found: {normalized_name}")

            self._default_provider_name = normalized_name

    def get_default(self) -> AIProvider:
        with self._lock:
            if self._default_provider_name is None:
                raise ProviderNotFoundError("No default AI provider is registered")

            return self._providers[self._default_provider_name]

    def get_default_name(self) -> str:
        with self._lock:
            if self._default_provider_name is None:
                raise ProviderNotFoundError("No default AI provider is registered")

            return self._default_provider_name

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized_name = name.strip().lower()

        if not normalized_name:
            raise ValueError("Provider name cannot be empty")

        return normalized_name