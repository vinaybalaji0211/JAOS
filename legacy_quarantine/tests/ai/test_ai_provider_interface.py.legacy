import pytest

from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


class DummyProvider(AIProviderInterface):
    @property
    def provider_name(self) -> str:
        return "dummy"

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse(
            success=True,
            content=f"Echo: {request.prompt}",
            provider=self.provider_name,
            model="dummy-model",
        )

    def health(self) -> AIProviderStatus:
        return AIProviderStatus.AVAILABLE


def test_provider_name():
    provider = DummyProvider()
    assert provider.provider_name == "dummy"


def test_provider_health():
    provider = DummyProvider()
    assert provider.health() == AIProviderStatus.AVAILABLE


def test_provider_generate():
    provider = DummyProvider()
    request = AIProviderRequest(prompt="Hello JAOS")

    response = provider.generate(request)

    assert response.success is True
    assert response.content == "Echo: Hello JAOS"
    assert response.provider == "dummy"
    assert response.model == "dummy-model"


def test_interface_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AIProviderInterface()