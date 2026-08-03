"""Tests for the Decision Platform domain models."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from jaos.intelligence.models.decision_confidence import (
    DecisionConfidence,
)
from jaos.intelligence.models.decision_priority import (
    DecisionPriority,
)
from jaos.intelligence.models.decision_proposal import (
    DecisionProposal,
)
from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)
from jaos.intelligence.models.decision_status import (
    DecisionStatus,
)
from jaos.intelligence.models.decision_strategy import (
    DecisionStrategy,
)
from jaos.intelligence.models.failure_behavior import (
    FailureBehavior,
)
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.intelligence_scope import (
    IntelligenceScope,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)
from jaos.intelligence.models.proposal_status import (
    ProposalStatus,
)
from jaos.intelligence.models.proposed_plan_step import (
    ProposedPlanStep,
)
from jaos.intelligence.models.risk_level import (
    RiskLevel,
)

# ------------------------------------------------------------------
# Helper Builders
# ------------------------------------------------------------------


def _identity() -> IntelligenceIdentity:
    """Create a valid IntelligenceIdentity."""

    return IntelligenceIdentity(
        scope=IntelligenceScope.SESSION,
        identity_id="session-001",
    )


def _step() -> ProposedPlanStep:
    """Create a valid ProposedPlanStep."""

    return ProposedPlanStep(
        description="Execute the task.",
        step_order=1,
        required_capability="planning",
        expected_output="Task completed.",
        success_condition="Execution succeeds.",
        failure_behavior=FailureBehavior.STOP,
        risk_level=RiskLevel.NONE,
    )


def _plan() -> PlanProposal:
    """Create a valid PlanProposal."""

    return PlanProposal(
        planning_id="planning-001",
        request_id="request-001",
        goal="Complete the objective.",
        identity=_identity(),
        steps=(_step(),),
        expected_outcomes=("Objective completed.",),
        success_criteria=("Execution finished successfully.",),
        status=ProposalStatus.DRAFT,
        risk_level=RiskLevel.NONE,
        confidence=1.0,
    )


def _request() -> DecisionRequest:
    """Create a valid DecisionRequest."""

    return DecisionRequest(
        identity=_identity(),
        plan_proposal=_plan(),
    )


def _proposal() -> DecisionProposal:
    """Create a valid DecisionProposal."""

    return DecisionProposal(
        request_id="request-001",
        identity=_identity(),
        plan_proposal=_plan(),
        decision_summary="Plan approved.",
        decision_rationale="Planning satisfies all constraints.",
    )


# ------------------------------------------------------------------
# DecisionRequest
# ------------------------------------------------------------------


def test_decision_request_defaults() -> None:
    """DecisionRequest should use the documented defaults."""

    plan = _plan()

    request = DecisionRequest(
        identity=_identity(),
        plan_proposal=plan,
    )

    assert request.identity == _identity()
    assert request.plan_proposal is plan
    assert request.decision_strategy is DecisionStrategy.ADAPTIVE
    assert request.priority is DecisionPriority.NORMAL
    assert request.metadata == {}
    assert request.planning_id == "planning-001"


def test_decision_request_to_dict() -> None:
    """DecisionRequest should serialize correctly."""

    request = _request()

    data = request.to_dict()

    assert data["request_id"] == request.request_id
    assert data["planning_id"] == "planning-001"
    assert data["decision_strategy"] == "adaptive"
    assert data["priority"] == "normal"
    assert isinstance(data["identity"], dict)
    assert isinstance(data["plan_proposal"], dict)
    assert isinstance(data["metadata"], dict)


@pytest.mark.parametrize(
    "request_id",
    [
        "",
        "   ",
    ],
)
def test_decision_request_rejects_invalid_request_id(
    request_id: str,
) -> None:
    """request_id must be a non-empty string."""

    with pytest.raises(ValueError):
        DecisionRequest(
            request_id=request_id,
            identity=_identity(),
            plan_proposal=_plan(),
        )


def test_decision_request_requires_identity() -> None:
    """identity must be an IntelligenceIdentity."""

    with pytest.raises(TypeError):
        DecisionRequest(
            identity=None,
            plan_proposal=_plan(),
        )


def test_decision_request_requires_plan_proposal() -> None:
    """plan_proposal must be a PlanProposal."""

    with pytest.raises(TypeError):
        DecisionRequest(
            identity=_identity(),
            plan_proposal=None,
        )


def test_decision_request_requires_strategy() -> None:
    """decision_strategy must be a DecisionStrategy."""

    with pytest.raises(TypeError):
        DecisionRequest(
            identity=_identity(),
            plan_proposal=_plan(),
            decision_strategy="adaptive",
        )


def test_decision_request_requires_priority() -> None:
    """priority must be a DecisionPriority."""

    with pytest.raises(TypeError):
        DecisionRequest(
            identity=_identity(),
            plan_proposal=_plan(),
            priority="normal",
        )


def test_decision_request_requires_dictionary_metadata() -> None:
    """metadata must be a dictionary."""

    with pytest.raises(TypeError):
        DecisionRequest(
            identity=_identity(),
            plan_proposal=_plan(),
            metadata=[],
        )


def test_decision_request_requires_timezone() -> None:
    """created_at must be timezone aware."""

    with pytest.raises(ValueError):
        DecisionRequest(
            identity=_identity(),
            plan_proposal=_plan(),
            created_at=datetime.now(),
        )


def test_decision_request_accepts_timezone() -> None:
    """Timezone-aware datetimes should be accepted."""

    request = DecisionRequest(
        identity=_identity(),
        plan_proposal=_plan(),
        created_at=datetime.now(timezone.utc),
    )

    assert request.created_at.tzinfo is not None
