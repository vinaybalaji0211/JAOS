"""Tests for the JAOS Planning Engine."""

from __future__ import annotations

import pytest

from jaos.intelligence.exceptions import (
    IntelligenceValidationError,
)
from jaos.intelligence.models import (
    ContextBundle,
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
    PlanningRequest,
    PlanProposal,
    ProposalStatus,
    ReasoningRequest,
    ReasoningResult,
)
from jaos.intelligence.planning import (
    DefaultPlanningEngine,
)
from jaos.intelligence.planning.planning_dependency_resolver import (
    PlanningDependencyResolver,
)
from jaos.intelligence.planning.planning_proposal_validator import (
    PlanningProposalValidator,
)
from jaos.intelligence.planning.planning_request_validator import (
    PlanningRequestValidator,
)
from jaos.intelligence.planning.planning_step_generator import (
    PlanningStepGenerator,
)
from jaos.intelligence.planning.planning_strategy_selector import (
    PlanningStrategySelector,
)


def build_identity() -> IntelligenceIdentity:
    """Build a reusable identity."""

    return IntelligenceIdentity(
        scope=IntelligenceScope.USER,
        identity_id="vinay",
    )


def build_reasoning_result() -> ReasoningResult:
    """Build a deterministic reasoning result."""

    identity = build_identity()

    request = IntelligenceRequest(
        objective="Build planning engine",
        request_type=IntelligenceRequestType.PLANNING,
        identity=identity,
    )

    context_item = ContextItem(
        context_type=IntelligenceContextType.USER,
        content="User is implementing JAOS.",
        identity=identity,
        source="tests",
        trust_level=ContextTrustLevel.USER_PROVIDED,
        estimated_tokens=8,
    )

    context_bundle = ContextBundle(
        request_id=request.request_id,
        identity=identity,
        items=(context_item,),
        max_tokens=256,
    )

    reasoning_request = ReasoningRequest(
        request_id=request.request_id,
        objective=request.objective,
        context_bundle=context_bundle,
    )

    return ReasoningResult(
        request_id=reasoning_request.request_id,
        objective_interpretation="Implement Planning Engine",
        reasoning_summary="Deterministic planning",
        confidence=1.0,
    )


def build_planning_request() -> PlanningRequest:
    """Build a reusable planning request."""

    identity = build_identity()

    reasoning_result = build_reasoning_result()

    return PlanningRequest(
        request_id=reasoning_result.request_id,
        identity=identity,
        goal="Implement Planning Engine",
        reasoning_result=reasoning_result,
        success_criteria=("Planning engine completed",),
    )


@pytest.fixture()
def engine() -> DefaultPlanningEngine:
    """Create a Planning Engine."""

    return DefaultPlanningEngine()


@pytest.fixture()
def planning_request() -> PlanningRequest:
    """Create a reusable planning request."""

    return build_planning_request()


# ---------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------


def test_default_engine_is_not_ready(
    engine: DefaultPlanningEngine,
) -> None:
    """The engine should start in the not-ready state."""

    assert engine.is_ready is False


def test_component_name_is_stable(
    engine: DefaultPlanningEngine,
) -> None:
    """The engine should expose a stable component name."""

    assert engine.component_name == "planning_engine"


# ---------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------


@pytest.mark.anyio
async def test_initialize_sets_ready_state(
    engine: DefaultPlanningEngine,
) -> None:
    """Initialization should make the engine ready."""

    assert engine.is_ready is False

    await engine.initialize()

    assert engine.is_ready is True


@pytest.mark.anyio
async def test_shutdown_clears_ready_state(
    engine: DefaultPlanningEngine,
) -> None:
    """Shutdown should clear the ready state."""

    await engine.initialize()

    assert engine.is_ready is True

    await engine.shutdown()

    assert engine.is_ready is False


@pytest.mark.anyio
async def test_initialize_and_shutdown_are_repeatable(
    engine: DefaultPlanningEngine,
) -> None:
    """Lifecycle operations should be deterministic."""

    await engine.initialize()
    assert engine.is_ready is True

    await engine.shutdown()
    assert engine.is_ready is False

    await engine.initialize()
    assert engine.is_ready is True


# ---------------------------------------------------------------------
# Planning Pipeline
# ---------------------------------------------------------------------


@pytest.mark.anyio
async def test_create_plan_returns_plan_proposal(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """The engine should return a PlanProposal."""

    await engine.initialize()

    proposal = await engine.create_plan(
        planning_request,
    )

    assert isinstance(
        proposal,
        PlanProposal,
    )


@pytest.mark.anyio
async def test_create_plan_returns_draft_proposal(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """Newly created plans should start in the DRAFT state."""

    await engine.initialize()

    proposal = await engine.create_plan(
        planning_request,
    )

    assert proposal.status is ProposalStatus.DRAFT


@pytest.mark.anyio
async def test_create_plan_preserves_request_identity(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """Planning should preserve request metadata."""

    await engine.initialize()

    proposal = await engine.create_plan(
        planning_request,
    )

    assert proposal.request_id == planning_request.request_id

    assert proposal.planning_id == planning_request.planning_id

    assert proposal.goal == planning_request.goal

    assert proposal.identity == planning_request.identity


@pytest.mark.anyio
async def test_create_plan_generates_single_step_v1(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """Version 1 should generate exactly one planning step."""

    await engine.initialize()

    proposal = await engine.create_plan(
        planning_request,
    )

    assert len(proposal.steps) == 1

    step = proposal.steps[0]

    assert step.step_order == 1

    assert step.description == planning_request.goal


@pytest.mark.anyio
async def test_create_plan_uses_request_success_criteria(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """Success criteria should be propagated into the proposal."""

    await engine.initialize()

    proposal = await engine.create_plan(
        planning_request,
    )

    assert proposal.success_criteria == planning_request.success_criteria


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------


@pytest.mark.anyio
async def test_create_plan_rejects_invalid_request(
    engine: DefaultPlanningEngine,
) -> None:
    """Invalid request types should be rejected."""

    await engine.initialize()

    with pytest.raises(
        (TypeError, IntelligenceValidationError),
    ):
        await engine.create_plan(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------


@pytest.mark.anyio
async def test_create_plan_is_deterministic(
    engine: DefaultPlanningEngine,
    planning_request: PlanningRequest,
) -> None:
    """Identical requests should produce equivalent plans."""

    await engine.initialize()

    proposal_one = await engine.create_plan(
        planning_request,
    )

    proposal_two = await engine.create_plan(
        planning_request,
    )

    assert proposal_one.goal == proposal_two.goal
    assert proposal_one.expected_outcomes == proposal_two.expected_outcomes
    assert proposal_one.success_criteria == proposal_two.success_criteria
    assert proposal_one.required_capabilities == proposal_two.required_capabilities

    assert len(proposal_one.steps) == len(proposal_two.steps)

    step_one = proposal_one.steps[0]
    step_two = proposal_two.steps[0]

    assert step_one.description == step_two.description
    assert step_one.required_capability == step_two.required_capability
    assert step_one.success_condition == step_two.success_condition


# ---------------------------------------------------------------------
# Dependency Injection
# ---------------------------------------------------------------------


class FakeRequestValidator(
    PlanningRequestValidator,
):

    def __init__(self) -> None:
        self.called = False

    def validate(
        self,
        request: PlanningRequest,
    ) -> PlanningRequest:
        self.called = True
        return request


class FakeStrategySelector(
    PlanningStrategySelector,
):
    def __init__(self) -> None:
        self.called = False

    def select(
        self,
        request: PlanningRequest,
    ):
        from jaos.intelligence.models.planning_strategy import (
            PlanningStrategy,
        )

        self.called = True
        return PlanningStrategy.DIRECT


class FakeStepGenerator(
    PlanningStepGenerator,
):
    def __init__(self, steps) -> None:
        self.called = False
        self._steps = steps

    def generate(
        self,
        request,
        strategy,
    ):
        self.called = True
        return self._steps


class FakeDependencyResolver(
    PlanningDependencyResolver,
):
    def __init__(self) -> None:
        self.called = False

    def resolve(
        self,
        steps,
    ):
        self.called = True
        return steps


class FakeProposalValidator(
    PlanningProposalValidator,
):
    def __init__(self, proposal) -> None:
        self.called = False
        self._proposal = proposal

    def validate(
        self,
        request,
        steps,
    ):
        self.called = True
        return self._proposal


@pytest.mark.anyio
async def test_dependency_injection_pipeline(
    planning_request: PlanningRequest,
) -> None:
    """Injected collaborators should be used by the engine."""

    validator = FakeRequestValidator()
    selector = FakeStrategySelector()

    real_engine = DefaultPlanningEngine()
    await real_engine.initialize()

    proposal = await real_engine.create_plan(
        planning_request,
    )

    generator = FakeStepGenerator(
        proposal.steps,
    )

    resolver = FakeDependencyResolver()

    proposal_validator = FakeProposalValidator(
        proposal,
    )

    engine = DefaultPlanningEngine(
        request_validator=validator,
        strategy_selector=selector,
        step_generator=generator,
        dependency_resolver=resolver,
        proposal_validator=proposal_validator,
    )

    await engine.initialize()

    result = await engine.create_plan(
        planning_request,
    )

    assert isinstance(result, PlanProposal)

    assert validator.called
    assert selector.called
    assert generator.called
    assert resolver.called
    assert proposal_validator.called
