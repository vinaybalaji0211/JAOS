"""AI response validation for the JAOS Conversation Engine."""

from __future__ import annotations

from typing import Any, TypeVar

from jaos.ai.provider.models import AIResponse
from jaos.ai.response.response_models import ParsedResponse
from jaos.intelligence.exceptions import IntelligenceConversationError

ConversationResponse = TypeVar(
    "ConversationResponse",
    AIResponse,
    ParsedResponse,
)


class ConversationProviderResponseValidator:
    """
    Validates responses crossing into the Conversation Engine.

    ParsedResponse is the official AIManager boundary response. AIResponse
    support is retained for lower-level tests and backward compatibility.
    """

    _COMPONENT = "conversation_response_validator"

    def __init__(
        self,
        *,
        max_text_characters: int | None = None,
    ) -> None:
        if max_text_characters is not None:
            if (
                isinstance(max_text_characters, bool)
                or not isinstance(max_text_characters, int)
            ):
                raise TypeError(
                    "max_text_characters must be an integer or None"
                )

            if max_text_characters < 1:
                raise ValueError(
                    "max_text_characters must be greater than zero"
                )

        self._max_text_characters = max_text_characters

    @property
    def max_text_characters(self) -> int | None:
        """Return the configured response-text limit."""

        return self._max_text_characters

    def validate(
        self,
        response: ConversationResponse,
        *,
        expected_provider: str | None = None,
        expected_model: str | None = None,
    ) -> ConversationResponse:
        """Validate and return the original response."""

        if not isinstance(response, (AIResponse, ParsedResponse)):
            raise TypeError(
                "response must be an AIResponse or ParsedResponse"
            )

        (
            text,
            provider,
            model,
            metadata,
            response_type,
        ) = self._extract_response_values(response)

        normalized_provider = self._normalize_expected_provider(
            expected_provider
        )
        normalized_model = self._normalize_expected_model(
            expected_model
        )

        self._validate_provider(
            provider=provider,
            expected_provider=normalized_provider,
            model=model,
            text=text,
            response_type=response_type,
        )
        self._validate_model(
            provider=provider,
            model=model,
            expected_model=normalized_model,
            text=text,
            response_type=response_type,
        )
        self._validate_text(
            text=text,
            provider=provider,
            model=model,
            response_type=response_type,
        )
        self._validate_metadata(
            metadata=metadata,
            text=text,
            provider=provider,
            model=model,
            response_type=response_type,
        )

        return response

    @staticmethod
    def _extract_response_values(
        response: AIResponse | ParsedResponse,
    ) -> tuple[
        str,
        str,
        str | None,
        dict[Any, Any],
        str,
    ]:
        if isinstance(response, AIResponse):
            return (
                response.text,
                response.provider,
                response.model,
                dict(response.metadata),
                "ai_response",
            )

        return (
            response.text,
            response.metadata.provider,
            response.metadata.model,
            dict(response.metadata.source_metadata),
            "parsed_response",
        )

    @staticmethod
    def _normalize_expected_provider(
        expected_provider: str | None,
    ) -> str | None:
        if expected_provider is None:
            return None

        if not isinstance(expected_provider, str):
            raise TypeError(
                "expected_provider must be a string or None"
            )

        normalized = expected_provider.strip().lower()

        if not normalized:
            raise ValueError(
                "expected_provider must not be empty"
            )

        return normalized

    @staticmethod
    def _normalize_expected_model(
        expected_model: str | None,
    ) -> str | None:
        if expected_model is None:
            return None

        if not isinstance(expected_model, str):
            raise TypeError(
                "expected_model must be a string or None"
            )

        normalized = expected_model.strip()

        if not normalized:
            raise ValueError(
                "expected_model must not be empty"
            )

        return normalized

    def _validate_provider(
        self,
        *,
        provider: str,
        expected_provider: str | None,
        model: str | None,
        text: str,
        response_type: str,
    ) -> None:
        if (
            expected_provider is not None
            and provider != expected_provider
        ):
            self._reject(
                "AI response provider does not match the selected provider",
                validation_rule="provider_match",
                provider=provider,
                model=model,
                text=text,
                response_type=response_type,
                expected_provider=expected_provider,
            )

    def _validate_model(
        self,
        *,
        provider: str,
        model: str | None,
        expected_model: str | None,
        text: str,
        response_type: str,
    ) -> None:
        if (
            expected_model is not None
            and model != expected_model
        ):
            self._reject(
                "AI response model does not match the selected model",
                validation_rule="model_match",
                provider=provider,
                model=model,
                text=text,
                response_type=response_type,
                expected_model=expected_model,
            )

    def _validate_text(
        self,
        *,
        text: str,
        provider: str,
        model: str | None,
        response_type: str,
    ) -> None:
        if "\x00" in text:
            self._reject(
                "AI response text contains a null character",
                validation_rule="safe_text",
                provider=provider,
                model=model,
                text=text,
                response_type=response_type,
            )

        if (
            self._max_text_characters is not None
            and len(text) > self._max_text_characters
        ):
            self._reject(
                "AI response text exceeds the configured character limit",
                validation_rule="text_length",
                provider=provider,
                model=model,
                text=text,
                response_type=response_type,
                max_text_characters=self._max_text_characters,
            )

    def _validate_metadata(
        self,
        *,
        metadata: dict[Any, Any],
        text: str,
        provider: str,
        model: str | None,
        response_type: str,
    ) -> None:
        for key in metadata:
            if not isinstance(key, str):
                self._reject(
                    "AI response metadata keys must be strings",
                    validation_rule="metadata_key_type",
                    provider=provider,
                    model=model,
                    text=text,
                    response_type=response_type,
                    invalid_key_type=type(key).__name__,
                )

            if not key.strip():
                self._reject(
                    "AI response metadata keys must not be empty",
                    validation_rule="metadata_key_content",
                    provider=provider,
                    model=model,
                    text=text,
                    response_type=response_type,
                )

    def _reject(
        self,
        message: str,
        *,
        validation_rule: str,
        provider: str,
        model: str | None,
        text: str,
        response_type: str,
        **details: Any,
    ) -> None:
        diagnostic_details: dict[str, Any] = {
            "validation_rule": validation_rule,
            "response_type": response_type,
            "provider": provider,
            "model": model,
            "text_length": len(text),
        }
        diagnostic_details.update(details)

        raise IntelligenceConversationError(
            message,
            component=self._COMPONENT,
            details=diagnostic_details,
        )