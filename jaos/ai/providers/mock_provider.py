from collections.abc import Generator

from jaos.ai.provider import (
    AIProvider,
    AIProviderCapabilities,
    AIProviderGenerationError,
    AIProviderHealth,
    AIProviderHealthStatus,
    AIProviderInfo,
    AIProviderNotInitializedError,
    AIRequest,
    AIResponse,
)


class MockProvider(AIProvider):
    """
    Deterministic AI provider for tests and offline development.
    """

    def __init__(
        self,
        *,
        name: str = "mock",
        model: str = "mock-model",
        response_prefix: str = "mock",
    ) -> None:
        self._name = name.strip().lower()
        self._model = model.strip()
        self._response_prefix = response_prefix.strip()
        self._initialized = False

        if not self._name:
            raise ValueError("Mock provider name cannot be empty")

        if not self._model:
            raise ValueError("Mock provider model cannot be empty")

    def initialize(self) -> None:
        self._initialized = True

    def shutdown(self) -> None:
        self._initialized = False

    def generate(self, request: AIRequest) -> AIResponse:
        self._ensure_initialized()

        if request.prompt.strip().lower() == "fail":
            raise AIProviderGenerationError("Mock provider forced failure")

        return AIResponse(
            text=f"{self._response_prefix}: {request.prompt}",
            model=request.model or self._model,
            provider=self._name,
        )

    def stream_generate(self, request: AIRequest) -> Generator[str, None, None]:
        self._ensure_initialized()

        response = f"{self._response_prefix}: {request.prompt}"

        for token in response.split():
            yield token

    def health(self) -> AIProviderHealth:
        if self._initialized:
            return AIProviderHealth(
                status=AIProviderHealthStatus.HEALTHY,
                message="Mock provider is initialized",
            )

        return AIProviderHealth(
            status=AIProviderHealthStatus.UNAVAILABLE,
            message="Mock provider is not initialized",
        )

    def provider_info(self) -> AIProviderInfo:
        return AIProviderInfo(
            name=self._name,
            version="1.0.0",
            models=(self._model,),
            capabilities=AIProviderCapabilities(
                supports_text_generation=True,
                supports_streaming=True,
                supports_tools=False,
                supports_vision=False,
                supports_audio=False,
            ),
        )

    def is_initialized(self) -> bool:
        return self._initialized

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            raise AIProviderNotInitializedError(
                f"AI provider is not initialized: {self._name}"
            )