import pytest

from jaos.ai.context import (
    ContextItem,
    ContextManager,
    ContextType,
    ConversationTurn,
)
from jaos.ai.prompt import PromptSectionType


def test_context_item_rejects_empty_content():
    with pytest.raises(ValueError):
        ContextItem(context_type=ContextType.SYSTEM, content="   ")


def test_conversation_turn_rejects_empty_role():
    with pytest.raises(ValueError):
        ConversationTurn(role="   ", content="hello")


def test_conversation_turn_rejects_empty_content():
    with pytest.raises(ValueError):
        ConversationTurn(role="user", content="   ")


def test_add_context_item():
    manager = ContextManager()
    item = ContextItem(
        context_type=ContextType.IDENTITY,
        content="You are JAOS.",
        priority=10,
    )

    manager.add_context(item)

    assert manager.list_context() == (item,)


def test_add_conversation_turn_normalizes_role_and_content():
    manager = ContextManager()

    manager.add_conversation_turn(" USER ", " hello ")

    turns = manager.list_conversation()

    assert len(turns) == 1
    assert turns[0].role == "user"
    assert turns[0].content == "hello"


def test_clear_context():
    manager = ContextManager()

    manager.add_context(ContextItem(ContextType.SYSTEM, "System rules"))
    manager.clear_context()

    assert manager.list_context() == ()


def test_clear_conversation():
    manager = ContextManager()

    manager.add_conversation_turn("user", "hello")
    manager.clear_conversation()

    assert manager.list_conversation() == ()


def test_clear_all():
    manager = ContextManager()

    manager.add_context(ContextItem(ContextType.SYSTEM, "System rules"))
    manager.add_conversation_turn("user", "hello")
    manager.clear_all()

    assert manager.list_context() == ()
    assert manager.list_conversation() == ()


def test_build_prompt_sections_from_context_items():
    manager = ContextManager()

    manager.add_context(
        ContextItem(
            context_type=ContextType.SYSTEM,
            content="System rules",
            priority=10,
        )
    )
    manager.add_context(
        ContextItem(
            context_type=ContextType.MEMORY,
            content="Memory info",
            priority=50,
        )
    )

    sections = manager.build_prompt_sections()

    assert len(sections) == 2
    assert sections[0].section_type == PromptSectionType.SYSTEM
    assert sections[0].content == "System rules"
    assert sections[1].section_type == PromptSectionType.MEMORY
    assert sections[1].content == "Memory info"


def test_build_prompt_sections_includes_conversation():
    manager = ContextManager()

    manager.add_conversation_turn("user", "hello")
    manager.add_conversation_turn("assistant", "hi")

    sections = manager.build_prompt_sections()

    assert len(sections) == 1
    assert sections[0].section_type == PromptSectionType.CONTEXT
    assert "user: hello" in sections[0].content
    assert "assistant: hi" in sections[0].content


def test_context_platform_integrates_with_prompt_sections():
    manager = ContextManager()

    manager.add_context(
        ContextItem(
            context_type=ContextType.IDENTITY,
            content="You are JAOS.",
            priority=20,
        )
    )

    sections = manager.build_prompt_sections()

    assert sections[0].section_type == PromptSectionType.IDENTITY
    assert sections[0].content == "You are JAOS."