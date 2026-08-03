"""Tests for the Default Decision Engine."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from jaos.intelligence.decision.confidence_evaluator import (
    ConfidenceEvaluator,
)
from jaos.intelligence.decision.decision_request_validator import (
    DecisionRequestValidator,
)
from jaos.intelligence.decision.decision_strategy_selector import (
    DecisionStrategySelector,
)
from jaos.intelligence.decision.default_decision_engine import (
    DefaultDecisionEngine,
)
from jaos.intelligence.decision.permission_evaluator import (
    PermissionEvaluator,
)
from jaos.intelligence.decision.policy_evaluator import (
    PolicyEvaluator,
)
from jaos.intelligence.models.decision_confidence import (
    DecisionConfidence,
)
from jaos.intelligence.models.decision_proposal import (
    DecisionProposal,
)
from jaos.intelligence.models.decision_request import (
    DecisionRequest,
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


def _identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        scope=IntelligenceScope.SESSION,
        identity_id="session-001",
    )


def _step() -> ProposedPlanStep:
    return ProposedPlanStep(
        description="Execute task",
        step_order=1,
        required_capability="planning",
        expected_output="Done",
        success_condition="Success",
        failure_behavior=FailureBehavior.STOP,
        risk_level=RiskLevel.NONE,
    )


def _plan() -> PlanProposal:
    return PlanProposal(
        planning_id="planning-001",
        request_id="request-001",
        goal="Goal",
        identity=_identity(),
        steps=(_step(),),
        expected_outcomes=("Completed",),
        success_criteria=("Success",),
        status=ProposalStatus.DRAFT,
        risk_level=RiskLevel.NONE,
        confidence=1.0,
    )


def _request() -> DecisionRequest:
    return DecisionRequest(
        identity=_identity(),
        plan_proposal=_plan(),
    )


class FakeValidator(DecisionRequestValidator):
    def __init__(self) -> None:
        self.called = False

    def validate(
        self,
        request: DecisionRequest,
    ) -> DecisionRequest:
        self.called = True
        return request


class FakeStrategySelector(DecisionStrategySelector):
    def __init__(self) -> None:
        self.called = False

    def select(
        self,
        request: DecisionRequest,
    ) -> DecisionStrategy:
        self.called = True
        return request.decision_strategy


class FakePolicyEvaluator(PolicyEvaluator):
    def __init__(self) -> None:
        self.called = False

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> bool:
        self.called = True
        return True


class FakePermissionEvaluator(PermissionEvaluator):
    def __init__(self) -> None:
        self.called = False

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> bool:
        self.called = True
        return True


class FakeConfidenceEvaluator(ConfidenceEvaluator):
    def __init__(self) -> None:
        self.called = False

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> DecisionConfidence:
        self.called = True
        return DecisionConfidence.HIGH


# ------------------------------------------------------------------
# DefaultDecisionEngine
# ------------------------------------------------------------------


@pytest.mark.anyio
async def test_default_decision_engine_initialize() -> None:
    """The engine should become ready after initialization."""

    engine = DefaultDecisionEngine()

    assert engine.is_ready is False

    await engine.initialize()

    assert engine.is_ready is True


@pytest.mark.anyio
async def test_default_decision_engine_shutdown() -> None:
    """The engine should no longer be ready after shutdown."""

    engine = DefaultDecisionEngine()

    await engine.initialize()

    assert engine.is_ready is True

    await engine.shutdown()

    assert engine.is_ready is False


@pytest.mark.anyio
async def test_default_decision_engine_generates_proposal() -> None:
    """The engine should generate a DecisionProposal."""

    engine = DefaultDecisionEngine()

    await engine.initialize()

    request = _request()

    proposal = await engine.make_decision(request)

    assert isinstance(
        proposal,
        DecisionProposal,
    )

    assert proposal.approved is True

    assert proposal.confidence is DecisionConfidence.HIGH

    # The engine should preserve the request ID.
    assert proposal.request_id == request.request_id

    # The engine should preserve the planning ID.
    assert proposal.plan_proposal.planning_id == request.plan_proposal.planning_id


@pytest.mark.anyio
async def test_default_decision_engine_uses_injected_components() -> None:
    """All injected collaborators should be invoked."""

    validator = FakeValidator()

    selector = FakeStrategySelector()

    policy = FakePolicyEvaluator()

    permission = FakePermissionEvaluator()

    confidence = FakeConfidenceEvaluator()

    engine = DefaultDecisionEngine(
        request_validator=validator,
        strategy_selector=selector,
        policy_evaluator=policy,
        permission_evaluator=permission,
        confidence_evaluator=confidence,
    )

    await engine.initialize()

    proposal = await engine.make_decision(_request())

    assert isinstance(
        proposal,
        DecisionProposal,
    )

    assert validator.called is True

    assert selector.called is True

    assert policy.called is True

    assert permission.called is True

    assert confidence.called is True


# ------------------------------------------------------------------
# Error Handling
# ------------------------------------------------------------------


@pytest.mark.anyio
async def test_default_decision_engine_propagates_validation_errors() -> None:
    """Validation failures should not be swallowed."""

    class BrokenValidator(
        DecisionRequestValidator,
    ):
        def validate(
            self,
            request: DecisionRequest,
        ) -> DecisionRequest:
            raise ValueError("validation failed")

    engine = DefaultDecisionEngine(
        request_validator=BrokenValidator(),
    )

    await engine.initialize()

    with pytest.raises(
        ValueError,
        match="validation failed",
    ):
        await engine.make_decision(_request())


@pytest.mark.anyio
async def test_default_decision_engine_component_name() -> None:
    """The engine should expose a stable component name."""

    engine = DefaultDecisionEngine()

    assert engine.component_name == "default_decision_engine"
