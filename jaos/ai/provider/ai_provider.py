from abc import ABC, abstractmethod
from collections.abc import Generator

from jaos.ai.provider.health import AIProviderHealth
from jaos.ai.provider.models import AIRequest, AIResponse
from jaos.ai.provider.provider_info import AIProviderInfo


class AIProvider(ABC):
    """
    Base contract for all AI providers.

    Every provider such as Ollama, OpenAI, Gemini, Anthropic,
    or future local providers must implement this interface.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the provider."""

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the provider safely."""

    @abstractmethod
    def generate(self, request: AIRequest) -> AIResponse:
        """Generate a complete response."""

    @abstractmethod
    def stream_generate(self, request: AIRequest) -> Generator[str, None, None]:
        """Generate a streaming response."""

    @abstractmethod
    def health(self) -> AIProviderHealth:
        """Return provider health."""

    @abstractmethod
    def provider_info(self) -> AIProviderInfo:
        """Return provider metadata and capabilities."""