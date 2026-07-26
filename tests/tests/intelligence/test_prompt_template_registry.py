"""Tests for versioned intelligence prompt templates."""

import pytest

from jaos.ai.provider.provider_config import AIProviderCapability
from jaos.intelligence.exceptions import IntelligenceValidationError
from jaos.intelligence.prompt.prompt_template import (
    IntelligencePromptTemplate,
)
from jaos.intelligence.prompt.prompt_template_registry import (
    PromptTemplateRegistry,
)


def create_template(
    *,
    template_id: str = "general",
    version: str = "1.0",
    task_instruction: str = "Answer the user accurately.",
) -> IntelligencePromptTemplate:
    """Create a representative prompt template."""

    return IntelligencePromptTemplate(
        template_id=template_id,
        version=version,
        system_instruction="You are JAOS.",
        task_instruction=task_instruction,
        required_provider_capabilities=(
            AIProviderCapability.CHAT,
        ),
        default_output_schema={
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
            },
            "required": ["answer"],
        },
        metadata={"owner": "jaos"},
    )


def test_template_normalizes_values_and_builds_reference() -> None:
    template = IntelligencePromptTemplate(
        template_id=" General ",
        version="1.0",
        system_instruction=" System instruction ",
        task_instruction=" Task instruction ",
        required_provider_capabilities=("CHAT",),
    )

    assert template.template_id == "general"
    assert template.system_instruction == "System instruction"
    assert template.task_instruction == "Task instruction"
    assert template.required_provider_capabilities == (
        AIProviderCapability.CHAT,
    )
    assert template.reference == "general@1.0"


def test_template_serializes_provider_capabilities() -> None:
    template = create_template()

    serialized = template.to_dict()

    assert serialized["reference"] == "general@1.0"
    assert serialized["required_provider_capabilities"] == [
        "chat"
    ]
    assert serialized["default_output_schema"]["type"] == "object"
    assert serialized["metadata"] == {"owner": "jaos"}


@pytest.mark.parametrize(
    "version",
    ("1", "", "version"),
)
def test_template_rejects_invalid_versions(version: str) -> None:
    with pytest.raises(ValueError):
        create_template(version=version)


def test_template_rejects_empty_capability_requirements() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        IntelligencePromptTemplate(
            template_id="general",
            version="1.0",
            system_instruction="System",
            task_instruction="Task",
            required_provider_capabilities=(),
        )


def test_template_rejects_non_serializable_schema() -> None:
    with pytest.raises(
        ValueError,
        match="JSON serializable",
    ):
        IntelligencePromptTemplate(
            template_id="general",
            version="1.0",
            system_instruction="System",
            task_instruction="Task",
            default_output_schema={"value": object()},
        )


def test_registry_registers_and_resolves_default_template() -> None:
    registry = PromptTemplateRegistry()
    template = create_template()

    registry.register_template(template)

    assert registry.resolve_template("GENERAL") is template
    assert registry.get_template("general", "1.0") is template


def test_registry_resolves_exact_template_version() -> None:
    registry = PromptTemplateRegistry()
    first = create_template(version="1.0")
    second = create_template(version="2.0")

    registry.register_template(first)
    registry.register_template(second)

    assert registry.resolve_template("general") is first
    assert registry.resolve_template("general", "2.0") is second


def test_registry_rejects_duplicate_template_version() -> None:
    registry = PromptTemplateRegistry()
    registry.register_template(create_template())

    with pytest.raises(
        IntelligenceValidationError,
        match="already registered",
    ):
        registry.register_template(create_template())


def test_registry_can_replace_template_version() -> None:
    registry = PromptTemplateRegistry()
    original = create_template(task_instruction="Original")
    replacement = create_template(task_instruction="Replacement")

    registry.register_template(original)
    registry.register_template(replacement, replace=True)

    resolved = registry.resolve_template("general", "1.0")

    assert resolved is replacement
    assert resolved.task_instruction == "Replacement"


def test_registry_can_change_default_version() -> None:
    registry = PromptTemplateRegistry()
    first = create_template(version="1.0")
    second = create_template(version="2.0")

    registry.register_template(first)
    registry.register_template(second)
    registry.set_default_version("general", "2.0")

    assert registry.resolve_template("general") is second


def test_registry_unregisters_template_and_updates_default() -> None:
    registry = PromptTemplateRegistry()
    first = create_template(version="1.0")
    second = create_template(version="2.0")

    registry.register_template(first)
    registry.register_template(second)

    removed = registry.unregister_template("general", "1.0")

    assert removed is first
    assert registry.resolve_template("general") is second
    assert registry.contains("general", "1.0") is False


def test_registry_lists_templates_deterministically() -> None:
    registry = PromptTemplateRegistry()
    beta = create_template(
        template_id="beta",
        version="2.0",
    )
    alpha_second = create_template(
        template_id="alpha",
        version="2.0",
    )
    alpha_first = create_template(
        template_id="alpha",
        version="1.0",
    )

    registry.register_template(beta)
    registry.register_template(alpha_second)
    registry.register_template(alpha_first)

    assert registry.list_templates() == (
        alpha_first,
        alpha_second,
        beta,
    )
    assert registry.list_templates("alpha") == (
        alpha_first,
        alpha_second,
    )


def test_registry_contains_and_length_track_versions() -> None:
    registry = PromptTemplateRegistry()

    assert len(registry) == 0
    assert registry.contains("general") is False

    registry.register_template(create_template(version="1.0"))
    registry.register_template(create_template(version="2.0"))

    assert len(registry) == 2
    assert registry.contains("general") is True
    assert registry.contains("general", "1.0") is True
    assert registry.contains("general", "3.0") is False


def test_registry_rejects_missing_template_id() -> None:
    registry = PromptTemplateRegistry()

    with pytest.raises(
        IntelligenceValidationError,
        match="template not found",
    ):
        registry.resolve_template("missing")


def test_registry_rejects_missing_template_version() -> None:
    registry = PromptTemplateRegistry()
    registry.register_template(create_template())

    with pytest.raises(
        IntelligenceValidationError,
        match="version not found",
    ):
        registry.resolve_template("general", "9.0")