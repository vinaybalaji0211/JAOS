import pytest

from jaos.ai.provider import AIResponse
from jaos.ai.response import (
    ParsedResponse,
    ResponseManager,
    ResponseMetadata,
    ResponseParser,
)


def test_response_metadata_defaults():
    metadata = ResponseMetadata(provider="mock")

    assert metadata.provider == "mock"
    assert metadata.created_at is not None


def test_parsed_response_rejects_empty_text():
    with pytest.raises(ValueError):
        ParsedResponse(
            text="   ",
            metadata=ResponseMetadata(provider="mock"),
        )


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