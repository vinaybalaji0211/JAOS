import pytest

from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_manager import AIProviderManager
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


class DummyProvider(AIProviderInterface):
    def __init__(self, name: str = "dummy") -> None:
        self._name = name

    @property
    def provider_name(self) -> str:
        return self._name

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse(
            success=True,
            content=f"{self.provider_name}: {request.prompt}",
            provider=self.provider_name,
            model="dummy-model",
        )

    def health(self) -> AIProviderStatus:
        return AIProviderStatus.AVAILABLE


def test_register_provider():
    manager = AIProviderManager()
    provider = DummyProvider()

    manager.register_provider(provider)

    assert manager.has_provider("dummy") is True
    assert manager.get_provider("dummy") is provider


def test_register_invalid_provider():
    manager = AIProviderManager()

    with pytest.raises(TypeError):
        manager.register_provider(object())


def test_register_duplicate_provider():
    manager = AIProviderManager()
    provider = DummyProvider()

    manager.register_provider(provider)

    with pytest.raises(ValueError):
        manager.register_provider(provider)


def test_list_providers():
    manager = AIProviderManager()

    manager.register_provider(DummyProvider("one"))
    manager.register_provider(DummyProvider("two"))

    assert manager.list_providers() == ["one", "two"]


def test_unregister_provider():
    manager = AIProviderManager()
    provider = DummyProvider()

    manager.register_provider(provider)
    manager.unregister_provider("dummy")

    assert manager.has_provider("dummy") is False


def test_unregister_missing_provider():
    manager = AIProviderManager()

    with pytest.raises(KeyError):
        manager.unregister_provider("missing")


def test_get_missing_provider():
    manager = AIProviderManager()

    with pytest.raises(KeyError):
        manager.get_provider("missing")


def test_first_registered_provider_becomes_default():
    manager = AIProviderManager()
    provider = DummyProvider("first")

    manager.register_provider(provider)

    assert manager.get_default_provider() is provider


def test_set_default_provider():
    manager = AIProviderManager()
    first = DummyProvider("first")
    second = DummyProvider("second")

    manager.register_provider(first)
    manager.register_provider(second)
    manager.set_default_provider("second")

    assert manager.get_default_provider() is second


def test_set_missing_default_provider():
    manager = AIProviderManager()

    with pytest.raises(KeyError):
        manager.set_default_provider("missing")


def test_get_default_provider_when_empty():
    manager = AIProviderManager()

    with pytest.raises(RuntimeError):
        manager.get_default_provider()


def test_generate_with_default_provider():
    manager = AIProviderManager()
    manager.register_provider(DummyProvider("default"))

    response = manager.generate(AIProviderRequest(prompt="hello"))

    assert response.success is True
    assert response.content == "default: hello"
    assert response.provider == "default"


def test_generate_with_named_provider():
    manager = AIProviderManager()
    manager.register_provider(DummyProvider("one"))
    manager.register_provider(DummyProvider("two"))

    response = manager.generate(
        AIProviderRequest(prompt="hello"),
        provider_name="two",
    )

    assert response.success is True
    assert response.content == "two: hello"
    assert response.provider == "two"


def test_unregister_default_falls_back_to_next_provider():
    manager = AIProviderManager()
    first = DummyProvider("first")
    second = DummyProvider("second")

    manager.register_provider(first)
    manager.register_provider(second)
    manager.unregister_provider("first")

    assert manager.get_default_provider() is second