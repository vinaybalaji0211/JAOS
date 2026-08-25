"""Shared default AI provider bootstrap for composition roots.

The canonical PlatformComposition registers and initializes the default mock
provider here so its rollback-scoped registration logic has one owner.
"""

from __future__ import annotations

from jaos.ai.provider import AIProviderConfig, AIProviderType, ProviderManager
from jaos.ai.providers.mock_provider import MockProvider

DEFAULT_PROVIDER_NAME = "mock"


def initialize_default_provider(provider_manager: ProviderManager) -> None:
    """Register and initialize the default mock provider.

    Rollback-scoped: if initialize_provider() fails, the just-registered
    provider is unregistered and shut down directly, so no live provider
    survives a failed caller construction.
    """

    mock_provider = MockProvider()

    provider_manager.register_provider(
        mock_provider,
        AIProviderConfig(
            name=DEFAULT_PROVIDER_NAME,
            provider_type=AIProviderType.MOCK,
            default_model="mock-model",
        ),
        set_default=True,
    )

    try:
        provider_manager.initialize_provider(DEFAULT_PROVIDER_NAME)
    except Exception:
        provider_manager.unregister_provider(DEFAULT_PROVIDER_NAME)
        mock_provider.shutdown()
        raise


__all__ = [
    "DEFAULT_PROVIDER_NAME",
    "initialize_default_provider",
]
