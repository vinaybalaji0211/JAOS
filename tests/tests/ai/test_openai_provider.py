import json
import urllib.error

import pytest

from config.ai_config import OpenAIConfig
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)
from executive_brain.ai.providers.openai_provider import OpenAIProvider


class DummyHTTPResponse:
    def __init__(
        self,
        status: int = 200,
        body: dict | None = None,
    ) -> None:
        self.status = status
        self._body = body or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def read(self) -> bytes:
        return json.dumps(self._body).encode("utf-8")


def test_openai_provider_defaults(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    provider = OpenAIProvider()

    assert provider.provider_name == "openai"
    assert provider.model == "gpt-4.1-mini"
    assert provider.api_key_configured is True


def test_openai_provider_without_api_key_is_unavailable(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    provider = OpenAIProvider()

    assert provider.api_key_configured is False
    assert provider.health() == AIProviderStatus.UNAVAILABLE


def test_openai_provider_health_available_with_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    provider = OpenAIProvider()

    assert provider.health() == AIProviderStatus.AVAILABLE


def test_openai_provider_uses_custom_config_and_key():
    config = OpenAIConfig(
        default_model="custom-model",
        timeout_seconds=5,
    )

    provider = OpenAIProvider(
        config=config,
        api_key="custom-key",
    )

    assert provider.model == "custom-model"
    assert provider.api_key_configured is True


def test_openai_generate_success(monkeypatch):
    def fake_urlopen(request, timeout):
        return DummyHTTPResponse(
            status=200,
            body={
                "choices": [
                    {
                        "message": {
                            "content": "Hello from OpenAI",
                        }
                    }
                ]
            },
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OpenAIProvider(api_key="test-key")
    response = provider.generate(AIProviderRequest(prompt="Hello"))

    assert isinstance(response, AIProviderResponse)
    assert response.success is True
    assert response.content == "Hello from OpenAI"
    assert response.provider == "openai"
    assert response.model == "gpt-4.1-mini"
    assert response.metadata["raw"]["choices"][0]["message"]["content"] == (
        "Hello from OpenAI"
    )


def test_openai_generate_rejects_invalid_request():
    provider = OpenAIProvider(api_key="test-key")

    with pytest.raises(TypeError):
        provider.generate("not-a-request")


def test_openai_generate_rejects_empty_prompt():
    provider = OpenAIProvider(api_key="test-key")

    with pytest.raises(ValueError):
        provider.generate(AIProviderRequest(prompt="   "))


def test_openai_generate_without_api_key_raises_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    provider = OpenAIProvider()

    with pytest.raises(RuntimeError, match="OpenAI API key is not configured"):
        provider.generate(AIProviderRequest(prompt="Hello"))


def test_openai_generate_handles_connection_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("connection failed")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OpenAIProvider(api_key="test-key")

    with pytest.raises(RuntimeError, match="OpenAI provider is unavailable"):
        provider.generate(AIProviderRequest(prompt="Hello"))


def test_openai_generate_handles_invalid_json(monkeypatch):
    class InvalidJSONResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return None

        def read(self):
            return b"not-json"

    def fake_urlopen(request, timeout):
        return InvalidJSONResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OpenAIProvider(api_key="test-key")

    with pytest.raises(RuntimeError, match="OpenAI returned invalid JSON"):
        provider.generate(AIProviderRequest(prompt="Hello"))


def test_openai_generate_handles_invalid_response_format(monkeypatch):
    def fake_urlopen(request, timeout):
        return DummyHTTPResponse(
            status=200,
            body={"unexpected": "format"},
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OpenAIProvider(api_key="test-key")

    with pytest.raises(RuntimeError, match="OpenAI response format is invalid"):
        provider.generate(AIProviderRequest(prompt="Hello"))