from jaos.ai.provider import AIResponse


class ResponseValidationError(ValueError):
    """Raised when a provider response is invalid."""


class ResponseValidator:
    """
    Validates raw AI provider responses before normalization and parsing.
    """

    def validate(self, response: AIResponse) -> None:
        if not isinstance(response, AIResponse):
            raise TypeError("ResponseValidator expects an AIResponse instance")

        if not response.text.strip():
            raise ResponseValidationError("AI response text cannot be empty")

        if not response.provider.strip():
            raise ResponseValidationError("AI response provider cannot be empty")

        if response.model is not None and not response.model.strip():
            raise ResponseValidationError("AI response model cannot be empty")