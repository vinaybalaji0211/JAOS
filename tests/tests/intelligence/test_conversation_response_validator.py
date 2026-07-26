"""Tests for Conversation Engine provider-response validation."""

import pytest

from jaos.ai.provider.models import AIResponse
from jaos.intelligence import IntelligenceConversationError
from jaos.intelligence.conversation.conversation_response_validator import (
    ConversationProviderResponseValidator,
)


def create_response(
    *,
    text: str = "JAOS response",
    provider: str = "mock",
    model: str | None = "mock-model",
    metadata: dict | None = None,
) -> AIResponse:
    return AIResponse(
        text=text,
        provider=provider,
        model=model,
        metadata=metadata or {},
    )


def test_validator_defaults_to_unrestricted_text() -> None:
    validator = ConversationProviderResponseValidator()

    assert validator.max_text_characters is None


def test_validator_accepts_positive_text_limit() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=1000,
    )

    assert validator.max_text_characters == 1000


@pytest.mark.parametrize(
    "value",
    [
        True,
        1.5,
        "100",
    ],
)
def test_validator_rejects_invalid_text_limit_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_text_characters",
    ):
        ConversationProviderResponseValidator(
            max_text_characters=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
    ],
)
def test_validator_rejects_non_positive_text_limit(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        ConversationProviderResponseValidator(
            max_text_characters=value,
        )


def test_validate_rejects_invalid_response_type() -> None:
    validator = ConversationProviderResponseValidator()

    with pytest.raises(
        TypeError,
        match="AIResponse",
    ):
        validator.validate("invalid response")


def test_validate_returns_original_response() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response()

    validated = validator.validate(response)

    assert validated is response


def test_expected_provider_is_normalized() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(provider=" Mock ")

    validated = validator.validate(
        response,
        expected_provider=" MOCK ",
    )

    assert validated is response
    assert response.provider == "mock"


def test_provider_check_is_optional() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(provider="local")

    assert validator.validate(response) is response


@pytest.mark.parametrize(
    "value",
    [
        False,
        10,
    ],
)
def test_validate_rejects_invalid_expected_provider_type(
    value: object,
) -> None:
    validator = ConversationProviderResponseValidator()

    with pytest.raises(
        TypeError,
        match="expected_provider",
    ):
        validator.validate(
            create_response(),
            expected_provider=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_validate_rejects_empty_expected_provider(
    value: str,
) -> None:
    validator = ConversationProviderResponseValidator()

    with pytest.raises(
        ValueError,
        match="expected_provider",
    ):
        validator.validate(
            create_response(),
            expected_provider=value,
        )


def test_validate_rejects_provider_mismatch() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(provider="mock")

    with pytest.raises(
        IntelligenceConversationError,
        match="provider does not match",
    ):
        validator.validate(
            response,
            expected_provider="local",
        )


def test_expected_model_is_trimmed() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(model="model-a")

    validated = validator.validate(
        response,
        expected_model=" model-a ",
    )

    assert validated is response


def test_model_check_is_optional() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(model=None)

    assert validator.validate(response) is response


@pytest.mark.parametrize(
    "value",
    [
        False,
        10,
    ],
)
def test_validate_rejects_invalid_expected_model_type(
    value: object,
) -> None:
    validator = ConversationProviderResponseValidator()

    with pytest.raises(
        TypeError,
        match="expected_model",
    ):
        validator.validate(
            create_response(),
            expected_model=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_validate_rejects_empty_expected_model(
    value: str,
) -> None:
    validator = ConversationProviderResponseValidator()

    with pytest.raises(
        ValueError,
        match="expected_model",
    ):
        validator.validate(
            create_response(),
            expected_model=value,
        )


def test_validate_rejects_model_mismatch() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(model="model-a")

    with pytest.raises(
        IntelligenceConversationError,
        match="model does not match",
    ):
        validator.validate(
            response,
            expected_model="model-b",
        )


def test_model_matching_is_case_sensitive() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(model="Model-A")

    with pytest.raises(
        IntelligenceConversationError,
        match="model does not match",
    ):
        validator.validate(
            response,
            expected_model="model-a",
        )


def test_validate_rejects_null_character() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        text="unsafe\x00response",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="null character",
    ):
        validator.validate(response)


def test_validate_accepts_text_at_exact_limit() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=5,
    )
    response = create_response(text="12345")

    assert validator.validate(response) is response


def test_validate_rejects_text_above_limit() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=5,
    )
    response = create_response(text="123456")

    with pytest.raises(
        IntelligenceConversationError,
        match="exceeds the configured character limit",
    ):
        validator.validate(response)


def test_validate_rejects_non_string_metadata_key() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        metadata={10: "invalid"},
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="metadata keys must be strings",
    ):
        validator.validate(response)


def test_validate_rejects_empty_metadata_key() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        metadata={"": "invalid"},
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="metadata keys must not be empty",
    ):
        validator.validate(response)


def test_validate_rejects_whitespace_metadata_key() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        metadata={"   ": "invalid"},
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="metadata keys must not be empty",
    ):
        validator.validate(response)


def test_validate_accepts_structured_metadata_values() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        metadata={
            "tokens": 42,
            "cached": True,
            "trace": {
                "request_id": "request-1",
            },
            "warnings": ["none"],
        },
    )

    assert validator.validate(response) is response


def test_validate_accepts_unicode_response_text() -> None:
    validator = ConversationProviderResponseValidator()
    response = create_response(
        text="Hello Vinay — JAOS is ready 🤖",
    )

    assert validator.validate(response) is response


def test_validator_can_validate_multiple_responses() -> None:
    validator = ConversationProviderResponseValidator(
        max_text_characters=100,
    )
    first = create_response(
        text="First response",
        provider="mock",
    )
    second = create_response(
        text="Second response",
        provider="local",
    )

    assert validator.validate(first) is first
    assert validator.validate(second) is second