import json
import urllib.error

import pytest

from config.ai_config import OllamaConfig
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)
from executive_brain.ai.providers.ollama_provider import OllamaProvider


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


def test_ollama_provider_defaults():
    provider = OllamaProvider()

    assert provider.provider_name == "ollama"
    assert provider.model == "llama3"
    assert provider.base_url == "http://localhost:11434"


def test_ollama_provider_uses_custom_config():
    config = OllamaConfig(
        base_url="http://localhost:9999/",
        default_model="custom-model",
        timeout_seconds=5,
    )

    provider = OllamaProvider(config=config)

    assert provider.model == "custom-model"
    assert provider.base_url == "http://localhost:9999"


def test_ollama_health_available(monkeypatch):
    def fake_urlopen(request, timeout):
        return DummyHTTPResponse(status=200)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OllamaProvider()

    assert provider.health() == AIProviderStatus.AVAILABLE


def test_ollama_health_unavailable_on_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("connection failed")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OllamaProvider()

    assert provider.health() == AIProviderStatus.UNAVAILABLE


def test_ollama_generate_success(monkeypatch):
    def fake_urlopen(request, timeout):
        return DummyHTTPResponse(
            status=200,
            body={"response": "Hello from Ollama"},
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OllamaProvider()
    response = provider.generate(AIProviderRequest(prompt="Hello"))

    assert isinstance(response, AIProviderResponse)
    assert response.success is True
    assert response.content == "Hello from Ollama"
    assert response.provider == "ollama"
    assert response.model == "llama3"
    assert response.metadata["raw"] == {"response": "Hello from Ollama"}


def test_ollama_generate_rejects_invalid_request():
    provider = OllamaProvider()

    with pytest.raises(TypeError):
        provider.generate("not-a-request")


def test_ollama_generate_rejects_empty_prompt():
    provider = OllamaProvider()

    with pytest.raises(ValueError):
        provider.generate(AIProviderRequest(prompt="   "))


def test_ollama_generate_handles_connection_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.URLError("connection failed")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider = OllamaProvider()

    with pytest.raises(RuntimeError, match="Ollama provider is unavailable"):
        provider.generate(AIProviderRequest(prompt="Hello"))


def test_ollama_generate_handles_invalid_json(monkeypatch):
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

    provider = OllamaProvider()

    with pytest.raises(RuntimeError, match="Ollama returned invalid JSON"):
        provider.generate(AIProviderRequest(prompt="Hello"))