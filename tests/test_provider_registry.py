import pytest

from jaos.ai.provider import (
    AIProvider,
    AIProviderCapabilities,
    AIProviderHealth,
    AIProviderHealthStatus,
    AIProviderInfo,
    AIRequest,
    AIResponse,
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError,
    ProviderRegistry,
)


class MockProvider(AIProvider):
    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(text=f"mock: {request.prompt}", provider="mock")

    def stream_generate(self, request: AIRequest):
        yield f"mock: {request.prompt}"

    def health(self) -> AIProviderHealth:
        return AIProviderHealth(status=AIProviderHealthStatus.HEALTHY)

    def provider_info(self) -> AIProviderInfo:
        return AIProviderInfo(
            name="mock",
            version="1.0.0",
            models=("mock-model",),
            capabilities=AIProviderCapabilities(),
        )


def test_register_provider():
    registry = ProviderRegistry()
    provider = MockProvider()

    registry.register("mock", provider)

    assert registry.count() == 1
    assert registry.has("mock") is True
    assert registry.get("mock") is provider


def test_register_normalizes_provider_name():
    registry = ProviderRegistry()
    provider = MockProvider()

    registry.register("  MOCK  ", provider)

    assert registry.has("mock") is True
    assert registry.get("MOCK") is provider


def test_duplicate_provider_registration_fails():
    registry = ProviderRegistry()
    provider = MockProvider()

    registry.register("mock", provider)

    with pytest.raises(ProviderAlreadyRegisteredError):
        registry.register("mock", provider)


def test_get_missing_provider_fails():
    registry = ProviderRegistry()

    with pytest.raises(ProviderNotFoundError):
        registry.get("missing")


def test_unregister_provider():
    registry = ProviderRegistry()
    provider = MockProvider()

    registry.register("mock", provider)
    removed = registry.unregister("mock")

    assert removed is provider
    assert registry.count() == 0
    assert registry.has("mock") is False


def test_unregister_missing_provider_fails():
    registry = ProviderRegistry()

    with pytest.raises(ProviderNotFoundError):
        registry.unregister("missing")


def test_first_registered_provider_becomes_default():
    registry = ProviderRegistry()
    provider = MockProvider()

    registry.register("mock", provider)

    assert registry.get_default() is provider
    assert registry.get_default_name() == "mock"


def test_explicit_default_provider():
    registry = ProviderRegistry()
    provider_a = MockProvider()
    provider_b = MockProvider()

    registry.register("provider-a", provider_a)
    registry.register("provider-b", provider_b, set_default=True)

    assert registry.get_default() is provider_b
    assert registry.get_default_name() == "provider-b"


def test_set_default_provider():
    registry = ProviderRegistry()
    provider_a = MockProvider()
    provider_b = MockProvider()

    registry.register("provider-a", provider_a)
    registry.register("provider-b", provider_b)

    registry.set_default("provider-b")

    assert registry.get_default() is provider_b


def test_set_missing_default_provider_fails():
    registry = ProviderRegistry()

    with pytest.raises(ProviderNotFoundError):
        registry.set_default("missing")


def test_default_changes_when_default_provider_removed():
    registry = ProviderRegistry()
    provider_a = MockProvider()
    provider_b = MockProvider()

    registry.register("provider-a", provider_a)
    registry.register("provider-b", provider_b)

    removed = registry.unregister("provider-a")

    assert removed is provider_a
    assert registry.get_default() is provider_b
    assert registry.get_default_name() == "provider-b"


def test_get_default_without_provider_fails():
    registry = ProviderRegistry()

    with pytest.raises(ProviderNotFoundError):
        registry.get_default()


def test_list_provider_names_sorted():
    registry = ProviderRegistry()

    registry.register("zeta", MockProvider())
    registry.register("alpha", MockProvider())
    registry.register("beta", MockProvider())

    assert registry.list_provider_names() == ("alpha", "beta", "zeta")


def test_clear_registry():
    registry = ProviderRegistry()

    registry.register("mock", MockProvider())
    registry.clear()

    assert registry.count() == 0

    with pytest.raises(ProviderNotFoundError):
        registry.get_default()


def test_empty_provider_name_fails():
    registry = ProviderRegistry()

    with pytest.raises(ValueError):
        registry.register("   ", MockProvider())