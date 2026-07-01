import pytest

from jaos.ai.provider import (
    AIProviderConfig,
    AIProviderType,
    ProviderManager,
)
from jaos.ai.providers import MockProvider
from jaos.ai.routing import (
    ProviderRouter,
    RoutingRequest,
    RoutingStrategy,
)


def create_manager() -> ProviderManager:
    manager = ProviderManager()

    manager.register_provider(
        MockProvider(),
        AIProviderConfig(
            name="mock",
            provider_type=AIProviderType.MOCK,
        ),
        set_default=True,
    )

    return manager


def test_default_strategy():
    router = ProviderRouter(create_manager())

    provider = router.resolve_provider(
        RoutingRequest()
    )

    assert provider == "mock"


def test_explicit_strategy():
    router = ProviderRouter(create_manager())

    provider = router.resolve_provider(
        RoutingRequest(
            provider_name="Mock",
            strategy=RoutingStrategy.EXPLICIT,
        )
    )

    assert provider == "mock"


def test_explicit_requires_provider():
    router = ProviderRouter(create_manager())

    with pytest.raises(ValueError):
        router.resolve_provider(
            RoutingRequest(
                strategy=RoutingStrategy.EXPLICIT,
            )
        )


def test_local_first():
    router = ProviderRouter(create_manager())

    provider = router.resolve_provider(
        RoutingRequest(
            strategy=RoutingStrategy.LOCAL_FIRST,
        )
    )

    assert provider == "mock"


def test_cloud_first():
    router = ProviderRouter(create_manager())

    provider = router.resolve_provider(
        RoutingRequest(
            strategy=RoutingStrategy.CLOUD_FIRST,
        )
    )

    assert provider == "mock"