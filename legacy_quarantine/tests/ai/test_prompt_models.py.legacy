from executive_brain.ai.prompt.prompt_models import (
    PromptMessage,
    PromptRequest,
    PromptResponse,
    PromptRole,
)


def test_prompt_role_values():
    assert PromptRole.SYSTEM.value == "system"
    assert PromptRole.USER.value == "user"
    assert PromptRole.ASSISTANT.value == "assistant"


def test_prompt_message_creation():
    message = PromptMessage(
        role=PromptRole.USER,
        content="Hello JAOS",
    )

    assert message.role == PromptRole.USER
    assert message.content == "Hello JAOS"


def test_prompt_request_defaults_to_empty_messages():
    request = PromptRequest()

    assert request.messages == []


def test_prompt_response_creation():
    response = PromptResponse(
        prompt="USER:\nHello JAOS",
        message_count=1,
    )

    assert response.prompt == "USER:\nHello JAOS"
    assert response.message_count == 1
