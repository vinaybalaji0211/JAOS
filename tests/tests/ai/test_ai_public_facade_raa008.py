import jaos.ai as ai_facade
from jaos.ai import (
    AIManager,
    AIProvider,
    AIProviderConfig,
    AIProviderType,
    ProviderManager,
)
from jaos.ai.providers.mock_provider import MockProvider


def test_mock_provider_is_absent_from_jaos_ai_all() -> None:
    assert "MockProvider" not in ai_facade.__all__


def test_mock_provider_is_not_an_attribute_of_jaos_ai_facade() -> None:
    assert hasattr(ai_facade, "MockProvider") is False
    assert getattr(ai_facade, "MockProvider", None) is None


def test_mock_provider_remains_importable_from_concrete_module() -> None:
    provider = MockProvider()

    assert isinstance(provider, AIProvider)
    assert provider.provider_info().name == "mock"


def test_abstract_facade_exports_remain_available() -> None:
    assert "AIManager" in ai_facade.__all__
    assert "AIProvider" in ai_facade.__all__
    assert "AIProviderConfig" in ai_facade.__all__
    assert "AIProviderType" in ai_facade.__all__
    assert "ProviderManager" in ai_facade.__all__

    assert AIManager is ai_facade.AIManager
    assert AIProvider is ai_facade.AIProvider
    assert AIProviderConfig is ai_facade.AIProviderConfig
    assert AIProviderType is ai_facade.AIProviderType
    assert ProviderManager is ai_facade.ProviderManager
    assert AIProviderType.MOCK.value == "mock"
