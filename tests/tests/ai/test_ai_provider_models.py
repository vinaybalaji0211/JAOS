import pytest

from executive_brain.ai.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


def test_ai_provider_status_values():
    assert AIProviderStatus.AVAILABLE.value == "available"
    assert AIProviderStatus.UNAVAILABLE.value == "unavailable"
    assert AIProviderStatus.ERROR.value == "error"


def test_ai_provider_request_defaults():
    request = AIProviderRequest(prompt="Hello JAOS")

    assert request.prompt == "Hello JAOS"
    assert request.system_prompt == ""
    assert request.conversation == []
    assert request.parameters == {}


def test_ai_provider_request_with_values():
    request = AIProviderRequest(
        prompt="Hello",
        system_prompt="You are JAOS.",
        conversation=[{"role": "user", "content": "Hello"}],
        parameters={"temperature": 0.7},
    )

    assert request.prompt == "Hello"
    assert request.system_prompt == "You are JAOS."
    assert request.conversation == [{"role": "user", "content": "Hello"}]
    assert request.parameters == {"temperature": 0.7}


def test_ai_provider_response_defaults():
    response = AIProviderResponse(
        success=True,
        content="Hello Vinay",
        provider="test-provider",
        model="test-model",
    )

    assert response.success is True
    assert response.content == "Hello Vinay"
    assert response.provider == "test-provider"
    assert response.model == "test-model"
    assert response.metadata == {}


def test_ai_provider_response_with_metadata():
    response = AIProviderResponse(
        success=True,
        content="Done",
        provider="ollama",
        model="llama3",
        metadata={"tokens": 10},
    )

    assert response.metadata == {"tokens": 10}