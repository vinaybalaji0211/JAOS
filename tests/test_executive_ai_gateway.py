import pytest

from jaos.ai import (
    AIManager,
    AIProviderConfig,
    AIProviderType,
    MockProvider,
    ProviderManager,
)
from jaos.executive.ai import (
    ExecutiveAIGateway,
    ExecutiveAIRequest,
    ExecutiveAIResponse,
)


def build_ai_manager() -> AIManager:
    provider_manager = ProviderManager()

    provider_manager.register_provider(
        MockProvider(),
        AIProviderConfig(
            name="mock",
            provider_type=AIProviderType.MOCK,
            default_model="mock-model",
        ),
        set_default=True,
    )

    provider_manager.initialize_provider("mock")

    return AIManager(provider_manager)


def test_executive_ai_request_rejects_empty_goal():
    with pytest.raises(ValueError):
        ExecutiveAIRequest(goal="   ")


def test_executive_ai_gateway_asks_ai_platform():
    gateway = ExecutiveAIGateway(build_ai_manager())

    response = gateway.ask(
        ExecutiveAIRequest(goal="Explain JAOS AI integration")
    )

    assert isinstance(response, ExecutiveAIResponse)
    assert response.provider == "mock"
    assert response.model == "mock-model"
    assert "Explain JAOS AI integration" in response.text


def test_executive_ai_gateway_includes_context():
    gateway = ExecutiveAIGateway(build_ai_manager())

    response = gateway.ask(
        ExecutiveAIRequest(
            goal="Summarize this",
            context="JAOS is an AI operating system.",
        )
    )

    assert "Goal:" in response.text
    assert "Summarize this" in response.text
    assert "Context:" in response.text
    assert "JAOS is an AI operating system." in response.text


def test_executive_ai_gateway_rejects_invalid_request_type():
    gateway = ExecutiveAIGateway(build_ai_manager())

    with pytest.raises(TypeError):
        gateway.ask("invalid")  # type: ignore[arg-type]