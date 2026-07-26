"""Tests for JAOS AI Intelligence Platform exceptions."""

import pytest

from jaos.intelligence import (
    IntelligenceAgentError,
    IntelligenceApprovalRequiredError,
    IntelligenceComponentStateError,
    IntelligenceContextError,
    IntelligenceConversationError,
    IntelligenceExecutionProposalError,
    IntelligencePermissionError,
    IntelligencePlanningError,
    IntelligencePlatformError,
    IntelligenceReasoningError,
    IntelligenceRequestError,
    IntelligenceValidationError,
)


def test_base_intelligence_error() -> None:
    error = IntelligencePlatformError("Platform failure")

    assert str(error) == "Platform failure"
    assert error.message == "Platform failure"
    assert error.error_code == "intelligence_platform_error"
    assert error.component == "intelligence"
    assert error.request_id is None
    assert error.retryable is False
    assert error.details == {}


@pytest.mark.parametrize(
    (
        "error_type",
        "expected_code",
        "expected_component",
    ),
    [
        (
            IntelligenceValidationError,
            "intelligence_validation_error",
            "validation",
        ),
        (
            IntelligenceRequestError,
            "intelligence_request_error",
            "request",
        ),
        (
            IntelligenceContextError,
            "intelligence_context_error",
            "context",
        ),
        (
            IntelligenceConversationError,
            "intelligence_conversation_error",
            "conversation",
        ),
        (
            IntelligenceReasoningError,
            "intelligence_reasoning_error",
            "reasoning",
        ),
        (
            IntelligencePlanningError,
            "intelligence_planning_error",
            "planning",
        ),
        (
            IntelligenceAgentError,
            "intelligence_agent_error",
            "agent_orchestration",
        ),
        (
            IntelligenceExecutionProposalError,
            "intelligence_execution_proposal_error",
            "execution_proposal",
        ),
        (
            IntelligencePermissionError,
            "intelligence_permission_error",
            "permissions",
        ),
        (
            IntelligenceApprovalRequiredError,
            "intelligence_approval_required",
            "approval",
        ),
        (
            IntelligenceComponentStateError,
            "intelligence_component_state_error",
            "lifecycle",
        ),
    ],
)
def test_specialized_intelligence_errors(
    error_type: type[IntelligencePlatformError],
    expected_code: str,
    expected_component: str,
) -> None:
    error = error_type(
        "Operation failed",
        request_id="request-001",
        retryable=True,
        details={"attempt": 1},
    )

    assert isinstance(error, IntelligencePlatformError)
    assert error.error_code == expected_code
    assert error.component == expected_component
    assert error.request_id == "request-001"
    assert error.retryable is True
    assert error.details == {"attempt": 1}


def test_error_normalizes_text_fields() -> None:
    error = IntelligencePlanningError(
        "  Planning failed  ",
        request_id="  request-001  ",
        component="  custom-planner  ",
    )

    assert error.message == "Planning failed"
    assert error.request_id == "request-001"
    assert error.component == "custom-planner"


def test_error_allows_component_override() -> None:
    error = IntelligenceContextError(
        "Context unavailable",
        component="memory-context-adapter",
    )

    assert error.component == "memory-context-adapter"


def test_error_copies_details() -> None:
    details = {"provider": "mock"}
    error = IntelligenceReasoningError(
        "Reasoning failed",
        details=details,
    )

    details["provider"] = "changed"

    assert error.details == {"provider": "mock"}


def test_error_serialization() -> None:
    error = IntelligenceApprovalRequiredError(
        "Approval is required",
        request_id="request-001",
        retryable=False,
        details={"permission": "file.write"},
    )

    assert error.to_dict() == {
        "error_type": "IntelligenceApprovalRequiredError",
        "error_code": "intelligence_approval_required",
        "message": "Approval is required",
        "request_id": "request-001",
        "component": "approval",
        "retryable": False,
        "details": {"permission": "file.write"},
    }


def test_intelligence_error_can_be_raised_and_caught() -> None:
    with pytest.raises(IntelligencePlatformError) as captured:
        raise IntelligencePlanningError("No valid plan available")

    assert isinstance(captured.value, IntelligencePlanningError)
    assert str(captured.value) == "No valid plan available"


@pytest.mark.parametrize("message", ["", "   "])
def test_error_rejects_empty_message(message: str) -> None:
    with pytest.raises(ValueError):
        IntelligencePlatformError(message)


@pytest.mark.parametrize("message", [None, 42, object()])
def test_error_rejects_non_string_message(message: object) -> None:
    with pytest.raises(TypeError):
        IntelligencePlatformError(message)


def test_error_rejects_empty_request_id() -> None:
    with pytest.raises(ValueError):
        IntelligencePlatformError(
            "Failure",
            request_id="   ",
        )


def test_error_rejects_empty_component() -> None:
    with pytest.raises(ValueError):
        IntelligencePlatformError(
            "Failure",
            component="   ",
        )


def test_error_rejects_non_boolean_retryable() -> None:
    with pytest.raises(TypeError):
        IntelligencePlatformError(
            "Failure",
            retryable="yes",
        )


def test_error_rejects_non_dictionary_details() -> None:
    with pytest.raises(TypeError):
        IntelligencePlatformError(
            "Failure",
            details=["invalid"],
        )