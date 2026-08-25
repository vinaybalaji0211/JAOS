import pytest

from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_manager import AIProviderManager
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)
from executive_brain.ai.routing.llm_router import LLMRouter


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


def build_router() -> LLMRouter:
    manager = AIProviderManager()
    manager.register_provider(DummyProvider("ollama"))
    manager.register_provider(DummyProvider("openai"))
    return LLMRouter(manager)


def test_router_requires_provider_manager():
    with pytest.raises(TypeError):
        LLMRouter(None)


def test_route_uses_default_provider():
    router = build_router()

    response = router.route(
        AIProviderRequest(prompt="Hello JAOS")
    )

    assert response.success is True
    assert response.provider == "ollama"
    assert response.content == "ollama: Hello JAOS"


def test_route_named_provider():
    router = build_router()

    response = router.route(
        AIProviderRequest(prompt="Hello JAOS"),
        provider_name="openai",
    )

    assert response.success is True
    assert response.provider == "openai"
    assert response.content == "openai: Hello JAOS"


def test_route_invalid_request():
    router = build_router()

    with pytest.raises(TypeError):
        router.route("invalid-request")


def test_route_empty_provider_name():
    router = build_router()

    with pytest.raises(ValueError):
        router.route(
            AIProviderRequest(prompt="Hello"),
            provider_name="",
        )


def test_route_unknown_provider():
    router = build_router()

    with pytest.raises(KeyError):
        router.route(
            AIProviderRequest(prompt="Hello"),
            provider_name="gemini",
        )


def test_default_provider_after_manager_change():
    manager = AIProviderManager()

    ollama = DummyProvider("ollama")
    openai = DummyProvider("openai")

    manager.register_provider(ollama)
    manager.register_provider(openai)

    manager.set_default_provider("openai")

    router = LLMRouter(manager)

    response = router.route(
        AIProviderRequest(prompt="Ping")
    )

    assert response.provider == "openai"
    assert response.content == "openai: Ping"