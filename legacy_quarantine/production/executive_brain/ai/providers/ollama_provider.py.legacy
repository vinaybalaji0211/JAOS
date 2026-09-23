"""
JAOS Ollama Provider

Phase 3 — JAOS-M-0026

Local Ollama provider implementation for JAOS Alpha.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from config.ai_config import OllamaConfig
from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


class OllamaProvider(AIProviderInterface):
    """
    AI provider implementation for a local Ollama server.
    """

    def __init__(self, config: OllamaConfig | None = None) -> None:
        self._config = config or OllamaConfig()

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model(self) -> str:
        return self._config.default_model

    @property
    def base_url(self) -> str:
        return self._config.base_url.rstrip("/")

    def health(self) -> AIProviderStatus:
        try:
            request = urllib.request.Request(
                url=f"{self.base_url}/api/tags",
                method="GET",
            )

            with urllib.request.urlopen(
                request,
                timeout=self._config.timeout_seconds,
            ) as response:
                if 200 <= response.status < 300:
                    return AIProviderStatus.AVAILABLE

            return AIProviderStatus.UNAVAILABLE

        except (urllib.error.URLError, TimeoutError, OSError):
            return AIProviderStatus.UNAVAILABLE

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        if not isinstance(request, AIProviderRequest):
            raise TypeError("request must be an AIProviderRequest")

        if not request.prompt.strip():
            raise ValueError("request prompt cannot be empty")

        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "stream": False,
        }

        payload.update(request.parameters)

        response_data = self._post_json("/api/generate", payload)

        content = str(response_data.get("response", ""))

        return AIProviderResponse(
            success=True,
            content=content,
            provider=self.provider_name,
            model=self.model,
            metadata={
                "raw": response_data,
            },
        )

    def _post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url=f"{self.base_url}{endpoint}",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self._config.timeout_seconds,
            ) as response:
                response_body = response.read().decode("utf-8")

                if not response_body:
                    return {}

                return json.loads(response_body)

        except urllib.error.HTTPError as error:
            raise RuntimeError(
                f"Ollama HTTP error: {error.code}"
            ) from error

        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise RuntimeError(
                "Ollama provider is unavailable"
            ) from error

        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Ollama returned invalid JSON"
            ) from error