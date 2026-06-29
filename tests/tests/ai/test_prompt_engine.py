import pytest

from executive_brain.ai.providers.ai_provider_models import AIProviderRequest
from executive_brain.ai.prompt.prompt_engine import PromptEngine
from executive_brain.ai.prompt.prompt_models import (
    PromptMessage,
    PromptRequest,
    PromptRole,
)


def test_build_prompt_with_single_user_message():
    engine = PromptEngine()

    request = PromptRequest(
        messages=[
            PromptMessage(
                role=PromptRole.USER,
                content="Hello JAOS",
            )
        ]
    )

    response = engine.build_prompt(request)

    assert response.prompt == "USER:\nHello JAOS"
    assert response.message_count == 1


def test_build_prompt_with_multiple_messages():
    engine = PromptEngine()

    request = PromptRequest(
        messages=[
            PromptMessage(role=PromptRole.SYSTEM, content="You are JAOS."),
            PromptMessage(role=PromptRole.USER, content="Hello"),
            PromptMessage(role=PromptRole.ASSISTANT, content="Ready."),
        ]
    )

    response = engine.build_prompt(request)

    assert response.prompt == (
        "SYSTEM:\nYou are JAOS.\n\n"
        "USER:\nHello\n\n"
        "ASSISTANT:\nReady."
    )
    assert response.message_count == 3


def test_build_prompt_strips_extra_whitespace():
    engine = PromptEngine()

    request = PromptRequest(
        messages=[
            PromptMessage(role=PromptRole.USER, content="   Hello JAOS   "),
        ]
    )

    response = engine.build_prompt(request)

    assert response.prompt == "USER:\nHello JAOS"


def test_to_provider_request():
    engine = PromptEngine()

    request = PromptRequest(
        messages=[
            PromptMessage(role=PromptRole.USER, content="Summarize this."),
        ]
    )

    provider_request = engine.to_provider_request(request)

    assert isinstance(provider_request, AIProviderRequest)
    assert provider_request.prompt == "USER:\nSummarize this."
    assert provider_request.parameters == {"message_count": 1}


def test_empty_prompt_request_raises_value_error():
    engine = PromptEngine()

    with pytest.raises(ValueError):
        engine.build_prompt(PromptRequest())


def test_invalid_request_type_raises_type_error():
    engine = PromptEngine()

    with pytest.raises(TypeError):
        engine.build_prompt("not-a-request")


def test_invalid_message_type_raises_type_error():
    engine = PromptEngine()

    request = PromptRequest(messages=["not-a-message"])

    with pytest.raises(TypeError):
        engine.build_prompt(request)


def test_empty_message_content_raises_value_error():
    engine = PromptEngine()

    request = PromptRequest(
        messages=[
            PromptMessage(role=PromptRole.USER, content="   "),
        ]
    )

    with pytest.raises(ValueError):
        engine.build_prompt(request)