"""Tests for AI Intelligence Platform reasoning models."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from jaos.intelligence import (
    ContextBundle,
    IntelligenceIdentity,
    IntelligenceScope,
    ReasoningAssumption,
    ReasoningRequest,
    ReasoningResult,
    RiskLevel,
)


@pytest.fixture
def user_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


@pytest.fixture
def context_bundle(
    user_identity: IntelligenceIdentity,
) -> ContextBundle:
    return ContextBundle(
        request_id="request-001",
        identity=user_identity,
        bundle_id="bundle-001",
    )


def test_reasoning_assumption_normalizes_valid_input() -> None:
    metadata = {"source": "context"}

    assumption = ReasoningAssumption(
        statement=" User approved execution ",
        confidence=1,
        assumption_id=" assumption-001 ",
        source_context_ids=(
            " context-001 ",
            "context-001",
            "context-002",
        ),
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert assumption.assumption_id == "assumption-001"
    assert assumption.statement == "User approved execution"
    assert assumption.confidence == 1.0
    assert assumption.source_context_ids == (
        "context-001",
        "context-002",
    )
    assert assumption.metadata == {"source": "context"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("assumption_id", ""),
        ("statement", "   "),
    ],
)
def test_reasoning_assumption_rejects_invalid_required_string(
    field_name: str,
    value: str,
) -> None:
    arguments: dict[str, object] = {
        "statement": "User approved execution",
        "confidence": 1.0,
        "assumption_id": "assumption-001",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        ReasoningAssumption(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize("confidence", [True, "0.5"])
def test_reasoning_assumption_rejects_invalid_confidence_type(
    confidence: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confidence must be a number",
    ):
        ReasoningAssumption(
            statement="User approved execution",
            confidence=confidence,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_reasoning_assumption_rejects_invalid_confidence_value(
    confidence: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="confidence must be between",
    ):
        ReasoningAssumption(
            statement="User approved execution",
            confidence=confidence,
        )


def test_reasoning_assumption_rejects_string_source_collection() -> None:
    with pytest.raises(
        TypeError,
        match="source_context_ids must be a collection",
    ):
        ReasoningAssumption(
            statement="User approved execution",
            confidence=1.0,
            source_context_ids="context-001",  # type: ignore[arg-type]
        )


def test_reasoning_assumption_rejects_empty_source_identifier() -> None:
    with pytest.raises(
        ValueError,
        match="source_context_ids must contain",
    ):
        ReasoningAssumption(
            statement="User approved execution",
            confidence=1.0,
            source_context_ids=("context-001", "   "),
        )


def test_reasoning_assumption_rejects_invalid_metadata() -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        ReasoningAssumption(
            statement="User approved execution",
            confidence=1.0,
            metadata=[],  # type: ignore[arg-type]
        )


def test_reasoning_assumption_to_dict_is_json_serializable() -> None:
    assumption = ReasoningAssumption(
        statement="User approved execution",
        confidence=0.9,
        assumption_id="assumption-001",
        source_context_ids=("context-001",),
    )

    decoded = json.loads(json.dumps(assumption.to_dict()))

    assert decoded == {
        "assumption_id": "assumption-001",
        "statement": "User approved execution",
        "confidence": 0.9,
        "source_context_ids": ["context-001"],
        "metadata": {},
    }


def test_reasoning_assumption_is_immutable() -> None:
    assumption = ReasoningAssumption(
        statement="User approved execution",
        confidence=1.0,
    )

    with pytest.raises(FrozenInstanceError):
        assumption.statement = "Changed"  # type: ignore[misc]


def test_reasoning_request_normalizes_valid_input(
    context_bundle: ContextBundle,
) -> None:
    metadata = {"source": "conversation"}

    request = ReasoningRequest(
        request_id=" request-001 ",
        objective=" Determine the next JAOS step ",
        context_bundle=context_bundle,
        reasoning_id=" reasoning-001 ",
        constraints=(
            " Preserve APIs ",
            "Preserve APIs",
            "No direct tool execution",
        ),
        required_output_type=" STRUCTURED ",
        risk_policy=" SAFE ",
        max_alternatives=2,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert request.request_id == "request-001"
    assert request.reasoning_id == "reasoning-001"
    assert request.objective == "Determine the next JAOS step"
    assert request.constraints == (
        "Preserve APIs",
        "No direct tool execution",
    )
    assert request.required_output_type == "structured"
    assert request.risk_policy == "safe"
    assert request.max_alternatives == 2
    assert request.metadata == {"source": "conversation"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("reasoning_id", ""),
        ("request_id", "   "),
        ("objective", ""),
        ("required_output_type", "   "),
        ("risk_policy", ""),
    ],
)
def test_reasoning_request_rejects_invalid_required_string(
    field_name: str,
    value: str,
    context_bundle: ContextBundle,
) -> None:
    arguments: dict[str, object] = {
        "request_id": "request-001",
        "objective": "Determine the next step",
        "context_bundle": context_bundle,
        "reasoning_id": "reasoning-001",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        ReasoningRequest(**arguments)  # type: ignore[arg-type]


def test_reasoning_request_rejects_invalid_context_bundle() -> None:
    with pytest.raises(
        TypeError,
        match="context_bundle must be an instance of ContextBundle",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle={},  # type: ignore[arg-type]
        )


def test_reasoning_request_rejects_mismatched_request_id(
    user_identity: IntelligenceIdentity,
) -> None:
    bundle = ContextBundle(
        request_id="another-request",
        identity=user_identity,
    )

    with pytest.raises(
        ValueError,
        match="context_bundle request_id must match request_id",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=bundle,
        )


@pytest.mark.parametrize("max_alternatives", [True, 1.5])
def test_reasoning_request_rejects_invalid_alternative_limit_type(
    max_alternatives: object,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_alternatives must be an integer",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            max_alternatives=max_alternatives,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("max_alternatives", [0, -1])
def test_reasoning_request_rejects_non_positive_alternative_limit(
    max_alternatives: int,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_alternatives must be greater than zero",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            max_alternatives=max_alternatives,
        )


def test_reasoning_request_rejects_string_constraint_collection(
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        TypeError,
        match="constraints must be a collection",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            constraints="Preserve APIs",  # type: ignore[arg-type]
        )


def test_reasoning_request_rejects_empty_constraint(
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        ValueError,
        match="constraints must contain only non-empty strings",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            constraints=("Preserve APIs", "   "),
        )


def test_reasoning_request_rejects_invalid_metadata(
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            metadata=[],  # type: ignore[arg-type]
        )


def test_reasoning_request_rejects_naive_created_at(
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        ReasoningRequest(
            request_id="request-001",
            objective="Determine the next step",
            context_bundle=context_bundle,
            created_at=datetime(2026, 1, 1),
        )


def test_reasoning_request_to_dict_is_json_serializable(
    context_bundle: ContextBundle,
) -> None:
    request = ReasoningRequest(
        request_id="request-001",
        objective="Determine the next step",
        context_bundle=context_bundle,
        reasoning_id="reasoning-001",
        constraints=("Preserve APIs",),
    )

    decoded = json.loads(json.dumps(request.to_dict()))

    assert decoded["reasoning_id"] == "reasoning-001"
    assert decoded["request_id"] == "request-001"
    assert decoded["constraints"] == ["Preserve APIs"]
    assert decoded["context_bundle"]["bundle_id"] == "bundle-001"


def test_reasoning_request_is_immutable(
    context_bundle: ContextBundle,
) -> None:
    request = ReasoningRequest(
        request_id="request-001",
        objective="Determine the next step",
        context_bundle=context_bundle,
    )

    with pytest.raises(FrozenInstanceError):
        request.objective = "Changed"  # type: ignore[misc]


def test_reasoning_result_normalizes_valid_input() -> None:
    assumption = ReasoningAssumption(
        statement="The architecture is approved",
        confidence=0.9,
        assumption_id="assumption-001",
    )
    metadata = {"provider": "mock"}

    result = ReasoningResult(
        request_id=" request-001 ",
        objective_interpretation=" Continue Phase 8 ",
        reasoning_summary=" Contracts must be completed first ",
        confidence=0.8,
        result_id=" result-001 ",
        assumptions=[assumption],  # type: ignore[arg-type]
        missing_information=(
            " Runtime version source ",
            "Runtime version source",
        ),
        alternatives=("Continue models", "Pause implementation"),
        risks=("Version drift",),
        constraints=("Preserve APIs",),
        risk_level=RiskLevel.LOW,
        recommended_next_action=" Complete models ",
        required_clarifications=("Confirm provider",),
        required_approvals=("tool_execution",),
        metadata=metadata,
    )

    metadata["provider"] = "changed"

    assert result.request_id == "request-001"
    assert result.result_id == "result-001"
    assert result.objective_interpretation == "Continue Phase 8"
    assert result.reasoning_summary == "Contracts must be completed first"
    assert result.confidence == 0.8
    assert result.assumptions == (assumption,)
    assert result.missing_information == ("Runtime version source",)
    assert result.risk_level is RiskLevel.LOW
    assert result.recommended_next_action == "Complete models"
    assert result.metadata == {"provider": "mock"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("result_id", ""),
        ("request_id", "   "),
        ("objective_interpretation", ""),
        ("reasoning_summary", "   "),
    ],
)
def test_reasoning_result_rejects_invalid_required_string(
    field_name: str,
    value: str,
) -> None:
    arguments: dict[str, object] = {
        "request_id": "request-001",
        "objective_interpretation": "Continue Phase 8",
        "reasoning_summary": "Complete contracts first",
        "confidence": 0.8,
        "result_id": "result-001",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        ReasoningResult(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize("confidence", [True, "0.8"])
def test_reasoning_result_rejects_invalid_confidence_type(
    confidence: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confidence must be a number",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=confidence,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_reasoning_result_rejects_confidence_outside_unit_interval(
    confidence: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="confidence must be between",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=confidence,
        )


def test_reasoning_result_rejects_invalid_assumption_type() -> None:
    with pytest.raises(
        TypeError,
        match="assumptions must contain only",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            assumptions=("invalid",),  # type: ignore[arg-type]
        )


def test_reasoning_result_rejects_duplicate_assumption_ids() -> None:
    first = ReasoningAssumption(
        statement="First",
        confidence=0.8,
        assumption_id="assumption-001",
    )
    second = ReasoningAssumption(
        statement="Second",
        confidence=0.7,
        assumption_id="assumption-001",
    )

    with pytest.raises(
        ValueError,
        match="assumption IDs must be unique",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            assumptions=(first, second),
        )


def test_reasoning_result_rejects_invalid_risk_level() -> None:
    with pytest.raises(
        TypeError,
        match="risk_level must be an instance of RiskLevel",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            risk_level="low",  # type: ignore[arg-type]
        )


def test_reasoning_result_rejects_invalid_recommended_action() -> None:
    with pytest.raises(
        TypeError,
        match="recommended_next_action must be a string or None",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            recommended_next_action=123,  # type: ignore[arg-type]
        )


def test_reasoning_result_rejects_string_text_collection() -> None:
    with pytest.raises(
        TypeError,
        match="risks must be a collection",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            risks="Version drift",  # type: ignore[arg-type]
        )


def test_reasoning_result_rejects_empty_text_item() -> None:
    with pytest.raises(
        ValueError,
        match="required_approvals must contain only",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            required_approvals=("tool_execution", "   "),
        )


def test_reasoning_result_rejects_invalid_metadata() -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            metadata=[],  # type: ignore[arg-type]
        )


def test_reasoning_result_rejects_naive_completed_at() -> None:
    with pytest.raises(
        ValueError,
        match="completed_at must be timezone-aware",
    ):
        ReasoningResult(
            request_id="request-001",
            objective_interpretation="Continue Phase 8",
            reasoning_summary="Complete contracts first",
            confidence=0.8,
            completed_at=datetime(2026, 1, 1),
        )


def test_reasoning_result_to_dict_is_json_serializable() -> None:
    assumption = ReasoningAssumption(
        statement="Architecture is approved",
        confidence=0.9,
        assumption_id="assumption-001",
    )

    result = ReasoningResult(
        request_id="request-001",
        objective_interpretation="Continue Phase 8",
        reasoning_summary="Complete contracts first",
        confidence=0.8,
        result_id="result-001",
        assumptions=(assumption,),
        risk_level=RiskLevel.LOW,
    )

    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["result_id"] == "result-001"
    assert decoded["request_id"] == "request-001"
    assert decoded["risk_level"] == "low"
    assert decoded["assumptions"][0]["assumption_id"] == (
        "assumption-001"
    )


def test_reasoning_result_is_immutable() -> None:
    result = ReasoningResult(
        request_id="request-001",
        objective_interpretation="Continue Phase 8",
        reasoning_summary="Complete contracts first",
        confidence=0.8,
    )

    with pytest.raises(FrozenInstanceError):
        result.confidence = 0.5  # type: ignore[misc]