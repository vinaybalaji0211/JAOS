class AIProviderError(Exception):
    """Base exception for AI provider errors."""


class AIProviderNotInitializedError(AIProviderError):
    """Raised when provider is used before initialization."""


class AIProviderInitializationError(AIProviderError):
    """Raised when provider initialization fails."""


class AIProviderGenerationError(AIProviderError):
    """Raised when provider fails to generate a response."""


class AIProviderShutdownError(AIProviderError):
    """Raised when provider shutdown fails."""