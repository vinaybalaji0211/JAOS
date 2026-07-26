"""Tests for prompt schema and capability support components."""

import pytest

from jaos.ai.provider.provider_config import (
    AIProviderCapability,
    AIProviderConfig,
)
from jaos.intelligence.prompt.prompt_output_schema_formatter import (
    PromptOutputSchemaFormatter,
    PromptOutputSchemaResult,
)
from jaos.intelligence.prompt.prompt_provider_capability_validator import (
    PromptProviderCapabilityResult,
    PromptProviderCapabilityValidator,
)


def create_schema() -> dict[str, object]:
    """Return a representative provider-neutral output schema."""

    return {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
        },
        "required": ["answer"],
        "additionalProperties": False,
    }


def test_output_schema_formatter_returns_deterministic_result() -> None:
    formatter = PromptOutputSchemaFormatter()

    first = formatter.format(create_schema())
    second = formatter.format(create_schema())

    assert isinstance(first, PromptOutputSchemaResult)
    assert first.content == second.content
    assert first.schema_hash == second.schema_hash
    assert len(first.schema_hash) == 64
    assert "Return only a valid JSON value" in first.content
    assert '"answer"' in first.content


def test_output_schema_formatter_sorts_schema_keys() -> None:
    formatter = PromptOutputSchemaFormatter()

    first = formatter.format({"z": 1, "a": 2})
    second = formatter.format({"a": 2, "z": 1})

    assert first.content == second.content
    assert first.schema_hash == second.schema_hash


def test_output_schema_result_to_dict_returns_copy() -> None:
    result = PromptOutputSchemaFormatter().format(create_schema())

    serialized = result.to_dict()
    serialized["schema"]["type"] = "changed"

    assert result.schema["type"] == "object"


def test_output_schema_formatter_rejects_empty_schema() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        PromptOutputSchemaFormatter().format({})


def test_output_schema_formatter_rejects_non_string_keys() -> None:
    with pytest.raises(
        TypeError,
        match="keys must be strings",
    ):
        PromptOutputSchemaFormatter().format({1: "invalid"})


def test_output_schema_formatter_rejects_unsupported_values() -> None:
    with pytest.raises(
        TypeError,
        match="unsupported value",
    ):
        PromptOutputSchemaFormatter().format(
            {"value": object()}
        )


def test_output_schema_formatter_rejects_non_finite_numbers() -> None:
    with pytest.raises(
        ValueError,
        match="non-finite number",
    ):
        PromptOutputSchemaFormatter().format(
            {"maximum": float("inf")}
        )


def test_capability_validator_preserves_provider_neutrality() -> None:
    validator = PromptProviderCapabilityValidator()

    result = validator.validate(
        (AIProviderCapability.CHAT,),
    )

    assert isinstance(result, PromptProviderCapabilityResult)
    assert result.validation_performed is False
    assert result.provider_name is None
    assert result.provider_enabled is None
    assert result.compatible is None
    assert result.missing_capabilities == ()


def test_capability_validator_accepts_compatible_provider() -> None:
    provider_config = AIProviderConfig(
        name="Local Provider",
        capabilities=(
            AIProviderCapability.CHAT,
            AIProviderCapability.TOOLS,
        ),
    )

    result = PromptProviderCapabilityValidator().validate(
        (
            AIProviderCapability.CHAT,
            AIProviderCapability.TOOLS,
        ),
        provider_config,
    )

    assert result.validation_performed is True
    assert result.provider_name == "local provider"
    assert result.provider_enabled is True
    assert result.compatible is True
    assert result.missing_capabilities == ()


def test_capability_validator_reports_missing_capabilities() -> None:
    provider_config = AIProviderConfig(
        name="Chat Provider",
        capabilities=(AIProviderCapability.CHAT,),
    )

    result = PromptProviderCapabilityValidator().validate(
        (
            AIProviderCapability.CHAT,
            AIProviderCapability.VISION,
        ),
        provider_config,
    )

    assert result.compatible is False
    assert result.supported_capabilities == (
        AIProviderCapability.CHAT,
    )
    assert result.missing_capabilities == (
        AIProviderCapability.VISION,
    )


def test_capability_validator_rejects_disabled_provider() -> None:
    provider_config = AIProviderConfig(
        name="Disabled Provider",
        enabled=False,
        capabilities=(AIProviderCapability.CHAT,),
    )

    result = PromptProviderCapabilityValidator().validate(
        (AIProviderCapability.CHAT,),
        provider_config,
    )

    assert result.provider_enabled is False
    assert result.compatible is False
    assert result.missing_capabilities == ()


def test_capability_validator_deduplicates_requirements() -> None:
    result = PromptProviderCapabilityValidator().validate(
        (
            AIProviderCapability.CHAT,
            AIProviderCapability.CHAT,
        )
    )

    assert result.required_capabilities == (
        AIProviderCapability.CHAT,
    )


def test_capability_validation_result_serializes_enums() -> None:
    provider_config = AIProviderConfig(
        name="Vision Provider",
        capabilities=(
            AIProviderCapability.CHAT,
            AIProviderCapability.VISION,
        ),
    )

    result = PromptProviderCapabilityValidator().validate(
        (AIProviderCapability.VISION,),
        provider_config,
    )

    assert result.to_dict() == {
        "required_capabilities": ["vision"],
        "provider_name": "vision provider",
        "provider_enabled": True,
        "supported_capabilities": ["vision"],
        "missing_capabilities": [],
        "validation_performed": True,
        "compatible": True,
    }