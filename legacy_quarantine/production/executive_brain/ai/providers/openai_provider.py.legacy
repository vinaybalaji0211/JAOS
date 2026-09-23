"""
JAOS OpenAI Provider

Phase 3 — JAOS-M-0027

Cloud OpenAI provider implementation for JAOS Alpha.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from config.ai_config import OpenAIConfig
from executive_brain.ai.providers.ai_provider_interface import AIProviderInterface
from executive_brain.ai.providers.ai_provider_models import (
    AIProviderRequest,
    AIProviderResponse,
    AIProviderStatus,
)


class OpenAIProvider(AIProviderInterface):
    """
    AI provider implementation for OpenAI chat completions.
    """

    def __init__(
        self,
        config: OpenAIConfig | None = None,
        api_key: str | None = None,
    ) -> None:
        self._config = config or OpenAIConfig()
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model(self) -> str:
        return self._config.default_model

    @property
    def api_key_configured(self) -> bool:
        return bool(self._api_key.strip())

    def health(self) -> AIProviderStatus:
        if not self.api_key_configured:
            return AIProviderStatus.UNAVAILABLE

        return AIProviderStatus.AVAILABLE

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        if not isinstance(request, AIProviderRequest):
            raise TypeError("request must be an AIProviderRequest")

        if not request.prompt.strip():
            raise ValueError("request prompt cannot be empty")

        if not self.api_key_configured:
            raise RuntimeError("OpenAI API key is not configured")

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
        }

        payload.update(request.parameters)

        response_data = self._post_json(
            endpoint="/v1/chat/completions",
            payload=payload,
        )

        content = self._extract_content(response_data)

        return AIProviderResponse(
            success=True,
            content=content,
            provider=self.provider_name,
            model=self.model,
            metadata={"raw": response_data},
        )

    def _post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url=f"https://api.openai.com{endpoint}",
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
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
                f"OpenAI HTTP error: {error.code}"
            ) from error

        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise RuntimeError(
                "OpenAI provider is unavailable"
            ) from error

        except json.JSONDecodeError as error:
            raise RuntimeError(
                "OpenAI returned invalid JSON"
            ) from error

    def _extract_content(self, response_data: dict[str, Any]) -> str:
        try:
            choices = response_data["choices"]
            first_choice = choices[0]
            message = first_choice["message"]
            content = message["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError("OpenAI response format is invalid") from error

        return str(content)