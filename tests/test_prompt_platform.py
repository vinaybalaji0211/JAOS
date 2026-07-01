import pytest

from jaos.ai.prompt import (
    PromptBuilder,
    PromptBuildRequest,
    PromptManager,
    PromptSection,
    PromptSectionType,
)


def test_prompt_section_rejects_empty_content():
    with pytest.raises(ValueError):
        PromptSection(
            section_type=PromptSectionType.SYSTEM,
            content="   ",
        )


def test_prompt_build_request_rejects_empty_user_prompt():
    with pytest.raises(ValueError):
        PromptBuildRequest(user_prompt="   ")


def test_prompt_builder_builds_user_only_prompt():
    builder = PromptBuilder()

    prompt = builder.build(PromptBuildRequest(user_prompt="Hello"))

    assert "[USER]" in prompt
    assert "Hello" in prompt


def test_prompt_builder_orders_sections_by_priority():
    builder = PromptBuilder()
    request = PromptBuildRequest(
        user_prompt="User question",
        sections=(
            PromptSection(
                section_type=PromptSectionType.MEMORY,
                content="Memory info",
                priority=50,
            ),
            PromptSection(
                section_type=PromptSectionType.SYSTEM,
                content="System rules",
                priority=10,
            ),
        ),
    )

    prompt = builder.build(request)

    assert prompt.index("[SYSTEM]") < prompt.index("[MEMORY]")
    assert prompt.index("[MEMORY]") < prompt.index("[USER]")


def test_prompt_manager_build_prompt():
    manager = PromptManager()

    prompt = manager.build_prompt(
        user_prompt="Explain JAOS",
        sections=(
            PromptSection(
                section_type=PromptSectionType.SYSTEM,
                content="You are JAOS.",
                priority=10,
            ),
        ),
    )

    assert "[SYSTEM]" in prompt
    assert "You are JAOS." in prompt
    assert "[USER]" in prompt
    assert "Explain JAOS" in prompt