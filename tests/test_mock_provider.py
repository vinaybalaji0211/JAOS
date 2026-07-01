import pytest

from jaos.ai.provider import (
    AIProviderGenerationError,
    AIProviderHealthStatus,
    AIProviderNotInitializedError,
    AIRequest,
)
from jaos.ai.providers import MockProvider


def test_mock_provider_rejects_empty_name():
    with pytest.raises(ValueError):
        MockProvider(name="   ")


def test_mock_provider_rejects_empty_model():
    with pytest.raises(ValueError):
        MockProvider(model="   ")


def test_mock_provider_initialization_lifecycle():
    provider = MockProvider()

    assert provider.is_initialized() is False

    provider.initialize()

    assert provider.is_initialized() is True

    provider.shutdown()

    assert provider.is_initialized() is False


def test_mock_provider_health_before_initialize():
    provider = MockProvider()

    health = provider.health()

    assert health.status == AIProviderHealthStatus.UNAVAILABLE
    assert "not initialized" in health.message


def test_mock_provider_health_after_initialize():
    provider = MockProvider()

    provider.initialize()
    health = provider.health()

    assert health.status == AIProviderHealthStatus.HEALTHY
    assert "initialized" in health.message


def test_mock_provider_generate_requires_initialization():
    provider = MockProvider()

    with pytest.raises(AIProviderNotInitializedError):
        provider.generate(AIRequest(prompt="hello"))


def test_mock_provider_generate():
    provider = MockProvider()

    provider.initialize()
    response = provider.generate(AIRequest(prompt="hello"))

    assert response.text == "mock: hello"
    assert response.provider == "mock"
    assert response.model == "mock-model"


def test_mock_provider_generate_uses_request_model():
    provider = MockProvider(model="default-model")

    provider.initialize()
    response = provider.generate(AIRequest(prompt="hello", model="custom-model"))

    assert response.model == "custom-model"


def test_mock_provider_forced_failure():
    provider = MockProvider()

    provider.initialize()

    with pytest.raises(AIProviderGenerationError):
        provider.generate(AIRequest(prompt="fail"))


def test_mock_provider_stream_generate():
    provider = MockProvider()

    provider.initialize()
    tokens = tuple(provider.stream_generate(AIRequest(prompt="hello world")))

    assert tokens == ("mock:", "hello", "world")


def test_mock_provider_info():
    provider = MockProvider(name="Mock", model="mock-model")

    info = provider.provider_info()

    assert info.name == "mock"
    assert info.version == "1.0.0"
    assert info.models == ("mock-model",)
    assert info.capabilities.supports_text_generation is True
    assert info.capabilities.supports_streaming is True