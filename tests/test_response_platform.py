import pytest

from jaos.ai.provider import AIResponse
from jaos.ai.response import (
    ParsedResponse,
    ResponseFinishReason,
    ResponseManager,
    ResponseMetadata,
    ResponseParser,
)


def test_response_metadata_defaults():
    metadata = ResponseMetadata(provider="mock")

    assert metadata.provider == "mock"
    assert metadata.finish_reason == ResponseFinishReason.UNKNOWN
    assert metadata.created_at is not None


def test_response_metadata_normalizes_provider_model_and_finish_reason():
    metadata = ResponseMetadata(
        provider=" MOCK ",
        model=" test-model ",
        finish_reason="stop",
    )

    assert metadata.provider == "mock"
    assert metadata.model == "test-model"
    assert metadata.finish_reason == ResponseFinishReason.STOP


def test_response_metadata_rejects_empty_provider():
    with pytest.raises(ValueError):
        ResponseMetadata(provider="   ")


def test_response_metadata_rejects_negative_latency():
    with pytest.raises(ValueError):
        ResponseMetadata(provider="mock", latency_seconds=-1)


def test_response_metadata_rejects_negative_token_count():
    with pytest.raises(ValueError):
        ResponseMetadata(provider="mock", token_count=-1)


def test_unknown_finish_reason_falls_back_to_unknown():
    metadata = ResponseMetadata(provider="mock", finish_reason="custom-reason")

    assert metadata.finish_reason == ResponseFinishReason.UNKNOWN


def test_parsed_response_rejects_empty_text():
    with pytest.raises(ValueError):
        ParsedResponse(
            text="   ",
            metadata=ResponseMetadata(provider="mock"),
        )


def test_parsed_response_status_helpers():
    complete = ParsedResponse(
        text="done",
        metadata=ResponseMetadata(
            provider="mock",
            finish_reason=ResponseFinishReason.STOP,
        ),
    )
    truncated = ParsedResponse(
        text="partial",
        metadata=ResponseMetadata(
            provider="mock",
            finish_reason=ResponseFinishReason.LENGTH,
        ),
    )
    error = ParsedResponse(
        text="error",
        metadata=ResponseMetadata(
            provider="mock",
            finish_reason=ResponseFinishReason.ERROR,
        ),
    )

    assert complete.is_complete() is True
    assert complete.is_truncated() is False
    assert complete.is_error() is False

    assert truncated.is_complete() is False
    assert truncated.is_truncated() is True
    assert truncated.is_error() is False

    assert error.is_complete() is False
    assert error.is_truncated() is False
    assert error.is_error() is True


def test_response_parser():
    parser = ResponseParser()

    parsed = parser.parse(
        AIResponse(
            text=" hello ",
            provider="mock",
        )
    )

    assert parsed.text == "hello"
    assert parsed.metadata.provider == "mock"
    assert parsed.metadata.finish_reason == ResponseFinishReason.UNKNOWN


def test_response_parser_preserves_metadata():
    parser = ResponseParser()

    parsed = parser.parse(
        AIResponse(
            text="response",
            provider="mock",
            model="mock-model",
            metadata={
                "latency_seconds": 0.1,
                "token_count": 5,
                "finish_reason": "stop",
                "custom": "value",
            },
        )
    )

    assert parsed.metadata.model == "mock-model"
    assert parsed.metadata.latency_seconds == 0.1
    assert parsed.metadata.token_count == 5
    assert parsed.metadata.finish_reason == ResponseFinishReason.STOP
    assert parsed.metadata.source_metadata["custom"] == "value"


def test_response_parser_rejects_invalid_response_type():
    parser = ResponseParser()

    with pytest.raises(TypeError):
        parser.parse("invalid")  # type: ignore[arg-type]


def test_response_manager():
    manager = ResponseManager()

    parsed = manager.process(
        AIResponse(
            text="response",
            provider="mock",
        )
    )

    assert parsed.text == "response"
    assert parsed.metadata.provider == "mock"