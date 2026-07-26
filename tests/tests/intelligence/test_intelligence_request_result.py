"""Tests for core AI Intelligence request and result models."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from jaos.intelligence import (
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceResult,
    IntelligenceResultStatus,
    IntelligenceScope,
)


@pytest.fixture
def user_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


def test_request_accepts_minimum_valid_input(
    user_identity: IntelligenceIdentity,
) -> None:
    request = IntelligenceRequest(
        objective=" Explain JAOS ",
        request_type=IntelligenceRequestType.CONVERSATION,
        identity=user_identity,
        request_id=" request-001 ",
    )

    assert request.objective == "Explain JAOS"
    assert request.request_id == "request-001"
    assert request.request_type is IntelligenceRequestType.CONVERSATION
    assert request.identity is user_identity
    assert request.created_at.tzinfo is not None


def test_request_normalizes_optional_values_and_collections(
    user_identity: IntelligenceIdentity,
) -> None:
    metadata = {"source": "cli"}

    request = IntelligenceRequest(
        objective="Build a plan",
        request_type=IntelligenceRequestType.PLANNING,
        identity=user_identity,
        session_id=" session-001 ",
        context_policy=" DEFAULT ",
        required_capabilities=(
            " Reasoning ",
            "reasoning",
            " MEMORY ",
        ),
        permission_constraints=(
            " Read ",
            "read",
            " Execute ",
        ),
        timeout_seconds=30,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert request.session_id == "session-001"
    assert request.context_policy == "default"
    assert request.required_capabilities == (
        "reasoning",
        "memory",
    )
    assert request.permission_constraints == (
        "read",
        "execute",
    )
    assert request.timeout_seconds == 30.0
    assert request.metadata == {"source": "cli"}


@pytest.mark.parametrize("objective", ["", "   ", None])
def test_request_rejects_invalid_objective(
    objective: str | None,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="objective must be a non-empty string",
    ):
        IntelligenceRequest(
            objective=objective,  # type: ignore[arg-type]
            request_type=IntelligenceRequestType.REASONING,
            identity=user_identity,
        )


@pytest.mark.parametrize("request_id", ["", "   ", None])
def test_request_rejects_invalid_request_id(
    request_id: str | None,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="request_id must be a non-empty string",
    ):
        IntelligenceRequest(
            objective="Reason about JAOS",
            request_type=IntelligenceRequestType.REASONING,
            identity=user_identity,
            request_id=request_id,  # type: ignore[arg-type]
        )


def test_request_rejects_invalid_request_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="request_type must be an instance",
    ):
        IntelligenceRequest(
            objective="Reason about JAOS",
            request_type="reasoning",  # type: ignore[arg-type]
            identity=user_identity,
        )


def test_request_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an instance",
    ):
        IntelligenceRequest(
            objective="Reason about JAOS",
            request_type=IntelligenceRequestType.REASONING,
            identity="vinay",  # type: ignore[arg-type]
        )


def test_request_rejects_invalid_session_id(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="session_id must be a string or None",
    ):
        IntelligenceRequest(
            objective="Continue conversation",
            request_type=IntelligenceRequestType.CONVERSATION,
            identity=user_identity,
            session_id=123,  # type: ignore[arg-type]
        )


def test_request_rejects_invalid_context_policy(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="context_policy must be a string or None",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            context_policy=123,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("timeout_seconds", [True, "30"])
def test_request_rejects_invalid_timeout_type(
    timeout_seconds: object,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="timeout_seconds must be a number or None",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            timeout_seconds=timeout_seconds,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("timeout_seconds", [0, -1])
def test_request_rejects_non_positive_timeout(
    timeout_seconds: float,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="timeout_seconds must be greater than zero",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            timeout_seconds=timeout_seconds,
        )


def test_request_rejects_invalid_metadata(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            metadata=[],  # type: ignore[arg-type]
        )


def test_request_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            created_at=datetime(2026, 1, 1),
        )


def test_request_rejects_string_as_capability_collection(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="required_capabilities must be a collection",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            required_capabilities="reasoning",  # type: ignore[arg-type]
        )


def test_request_rejects_empty_collection_item(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="permission_constraints must contain only",
    ):
        IntelligenceRequest(
            objective="Build context",
            request_type=IntelligenceRequestType.CONTEXT,
            identity=user_identity,
            permission_constraints=("read", "   "),
        )


def test_request_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
) -> None:
    request = IntelligenceRequest(
        objective="Create a plan",
        request_type=IntelligenceRequestType.PLANNING,
        identity=user_identity,
        request_id="request-001",
        required_capabilities=("reasoning",),
        metadata={"source": "test"},
    )

    encoded = json.dumps(request.to_dict())
    decoded = json.loads(encoded)

    assert decoded["request_id"] == "request-001"
    assert decoded["request_type"] == "planning"
    assert decoded["identity"] == {
        "scope": "user",
        "identity_id": "vinay",
    }
    assert decoded["required_capabilities"] == ["reasoning"]


def test_request_is_immutable(
    user_identity: IntelligenceIdentity,
) -> None:
    request = IntelligenceRequest(
        objective="Create a plan",
        request_type=IntelligenceRequestType.PLANNING,
        identity=user_identity,
    )

    with pytest.raises(FrozenInstanceError):
        request.objective = "Changed"  # type: ignore[misc]


def test_successful_result_accepts_text_output() -> None:
    result = IntelligenceResult(
        request_id=" request-001 ",
        status=IntelligenceResultStatus.SUCCEEDED,
        output=" Completed ",
        reasoning_summary=" Validated response ",
        assumptions=(" User approved ", "User approved"),
        risks=(" Low provider risk ",),
        confidence=0.9,
        provider_name=" OpenAI ",
        provider_model=" GPT ",
    )

    assert result.request_id == "request-001"
    assert result.output == "Completed"
    assert result.reasoning_summary == "Validated response"
    assert result.assumptions == ("User approved",)
    assert result.risks == ("Low provider risk",)
    assert result.confidence == 0.9
    assert result.provider_name == "openai"
    assert result.provider_model == "GPT"


def test_successful_result_accepts_structured_output() -> None:
    result = IntelligenceResult(
        request_id="request-001",
        status=IntelligenceResultStatus.SUCCEEDED,
        structured_output={"steps": ["inspect", "test"]},
    )

    assert result.output is None
    assert result.structured_output == {
        "steps": ["inspect", "test"],
    }


def test_successful_result_requires_output() -> None:
    with pytest.raises(
        ValueError,
        match="successful result must define output",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=IntelligenceResultStatus.SUCCEEDED,
        )


@pytest.mark.parametrize(
    "status",
    [
        IntelligenceResultStatus.FAILED,
        IntelligenceResultStatus.REJECTED,
    ],
)
def test_failed_or_rejected_result_requires_error_message(
    status: IntelligenceResultStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="must define error_message",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=status,
        )


def test_failed_result_normalizes_error_information() -> None:
    result = IntelligenceResult(
        request_id="request-001",
        status=IntelligenceResultStatus.FAILED,
        error_code=" PROVIDER_FAILURE ",
        error_message=" Provider unavailable ",
    )

    assert result.error_code == "provider_failure"
    assert result.error_message == "Provider unavailable"


def test_result_rejects_invalid_status() -> None:
    with pytest.raises(
        TypeError,
        match="status must be an instance",
    ):
        IntelligenceResult(
            request_id="request-001",
            status="succeeded",  # type: ignore[arg-type]
            output="Done",
        )


@pytest.mark.parametrize("confidence", [True, "0.5"])
def test_result_rejects_invalid_confidence_type(
    confidence: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confidence must be a number",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=IntelligenceResultStatus.PENDING,
            confidence=confidence,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_result_rejects_confidence_outside_unit_interval(
    confidence: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="confidence must be between",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=IntelligenceResultStatus.PENDING,
            confidence=confidence,
        )


def test_result_rejects_invalid_structured_output() -> None:
    with pytest.raises(
        TypeError,
        match="structured_output must be a dictionary",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=IntelligenceResultStatus.PENDING,
            structured_output=[],  # type: ignore[arg-type]
        )


def test_result_rejects_naive_completed_at() -> None:
    with pytest.raises(
        ValueError,
        match="completed_at must be timezone-aware",
    ):
        IntelligenceResult(
            request_id="request-001",
            status=IntelligenceResultStatus.PENDING,
            completed_at=datetime(2026, 1, 1),
        )


def test_result_to_dict_is_json_serializable() -> None:
    result = IntelligenceResult(
        request_id="request-001",
        result_id="result-001",
        status=IntelligenceResultStatus.SUCCEEDED,
        output="Done",
        proposed_actions=("Run tests",),
        required_approvals=("tool_execution",),
        confidence=1.0,
    )

    encoded = json.dumps(result.to_dict())
    decoded = json.loads(encoded)

    assert decoded["result_id"] == "result-001"
    assert decoded["request_id"] == "request-001"
    assert decoded["status"] == "succeeded"
    assert decoded["output"] == "Done"
    assert decoded["proposed_actions"] == ["Run tests"]
    assert decoded["required_approvals"] == ["tool_execution"]


def test_result_is_immutable() -> None:
    result = IntelligenceResult(
        request_id="request-001",
        status=IntelligenceResultStatus.SUCCEEDED,
        output="Done",
    )

    with pytest.raises(FrozenInstanceError):
        result.output = "Changed"  # type: ignore[misc]