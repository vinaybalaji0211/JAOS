"""Tests for ParsedResponse validation in the Conversation Engine."""

import pytest

from jaos.ai.response.response_models import (
    ParsedResponse,
    ResponseMetadata,
)
from jaos.intelligence import IntelligenceConversationError
from jaos.intelligence.conversation.conversation_response_validator import (
    ConversationProviderResponseValidator,
)


def create_parsed_response(
    *,
    text: str = "JAOS parsed response",
    provider: str = "mock",
    model: str | None = "mock-model",
    source_metadata: dict | None = None,
) -> ParsedResponse:
    return ParsedResponse(
        text=text,
        metadata=ResponseMetadata(
            provider=provider,
            model=model,
            source_metadata=source_metadata or {},
        ),
    )


def test_validate_returns_original_parsed_response() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response()

    validated = validator.validate(response)

    assert validated is response


def test_validate_matches_normalized_parsed_provider() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(provider=" Mock ")

    validated = validator.validate(
        response,
        expected_provider=" MOCK ",
    )

    assert validated is response
    assert response.metadata.provider == "mock"


def test_validate_matches_trimmed_parsed_model() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(model=" model-a ")

    validated = validator.validate(
        response,
        expected_model=" model-a ",
    )

    assert validated is response
    assert response.metadata.model == "model-a"


def test_validate_accepts_parsed_response_without_model() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(model=None)

    assert validator.validate(response) is response


def test_validate_rejects_parsed_provider_mismatch() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(provider="mock")

    with pytest.raises(
        IntelligenceConversationError,
        match="provider does not match",
    ):
        validator.validate(
            response,
            expected_provider="local",
        )


def test_validate_rejects_parsed_model_mismatch() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(model="model-a")

    with pytest.raises(
        IntelligenceConversationError,
        match="model does not match",
    ):
        validator.validate(
            response,
            expected_model="model-b",
        )


def test_validate_rejects_null_character_in_parsed_text() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(
        text="unsafe\x00response",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="null character",
    ):
        validator.validate(response)


def test_validate_accepts_parsed_text_at_exact_limit() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=5,
    )
    response = create_parsed_response(text="12345")

    assert validator.validate(response) is response


def test_validate_rejects_parsed_text_above_limit() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=5,
    )
    response = create_parsed_response(text="123456")

    with pytest.raises(
        IntelligenceConversationError,
        match="exceeds the configured character limit",
    ):
        validator.validate(response)


def test_validate_rejects_non_string_parsed_metadata_key() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(
        source_metadata={10: "invalid"},
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="metadata keys must be strings",
    ):
        validator.validate(response)


@pytest.mark.parametrize(
    "key",
    [
        "",
        "   ",
    ],
)
def test_validate_rejects_empty_parsed_metadata_key(
    key: str,
) -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(
        source_metadata={key: "invalid"},
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="metadata keys must not be empty",
    ):
        validator.validate(response)


def test_validate_accepts_structured_parsed_metadata() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_parsed_response(
        source_metadata={
            "token_count": 42,
            "cached": True,
            "trace": {
                "request_id": "request-1",
            },
            "warnings": ["none"],
        },
    )

    assert validator.validate(response) is response