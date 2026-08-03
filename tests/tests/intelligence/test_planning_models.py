"""Tests for JAOS AI Intelligence Planning Platform."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest

from jaos.intelligence import (
    FailureBehavior,
    IntelligenceIdentity,
    IntelligenceScope,
    PlanningConfiguration,
    PlanningRequest,
    PlanProposal,
    ProposalStatus,
    ProposedPlanStep,
    ReasoningResult,
    RiskLevel,
)

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def user_identity() -> IntelligenceIdentity:
    """Return a reusable user identity."""

    return IntelligenceIdentity(
        scope=IntelligenceScope.USER,
        identity_id="vinay",
    )


@pytest.fixture
def reasoning_result() -> ReasoningResult:
    """Return a valid reasoning result."""

    return ReasoningResult(
        request_id="request-001",
        objective_interpretation="Continue Phase 8",
        reasoning_summary="Planning platform stabilization",
        confidence=0.95,
        result_id="reasoning-result-001",
    )


@pytest.fixture
def planning_configuration() -> PlanningConfiguration:
    """Return the default planning configuration."""

    return PlanningConfiguration()


# ============================================================================
# Helper Builders
# ============================================================================


def build_step(
    **overrides: object,
) -> ProposedPlanStep:
    """
    Construct a valid ProposedPlanStep.

    Individual tests override only the fields they care about.
    """

    values: dict[str, object] = {
        "step_id": "step-001",
        "description": "Create planning models",
        "step_order": 1,
        "required_capability": "coding",
        "expected_output": "Validated planning models",
        "success_condition": "All unit tests pass",
        "dependencies": (),
        "suggested_tool_category": "filesystem",
        "input_references": (),
        "permission_requirements": (),
        "risk_level": RiskLevel.NONE,
        "failure_behavior": FailureBehavior.STOP,
        "metadata": {},
    }

    values.update(overrides)

    return ProposedPlanStep(**values)


def build_request(
    user_identity: IntelligenceIdentity,
    reasoning_result: ReasoningResult,
    planning_configuration: PlanningConfiguration,
    **overrides: object,
) -> PlanningRequest:
    """
    Construct a valid PlanningRequest.

    Tests override only the values under validation.
    """

    values: dict[str, object] = {
        "request_id": "request-001",
        "planning_id": "planning-001",
        "goal": "Complete Phase 8",
        "identity": user_identity,
        "reasoning_result": reasoning_result,
        "configuration": planning_configuration,
        "constraints": (),
        "permission_constraints": (),
        "success_criteria": ("All tests pass",),
        "metadata": {},
    }

    values.update(overrides)

    return PlanningRequest(**values)


def build_proposal(
    user_identity: IntelligenceIdentity,
    **overrides: object,
) -> PlanProposal:
    """
    Construct a valid PlanProposal.

    Tests override only the fields they need.
    """

    values: dict[str, object] = {
        "proposal_id": "proposal-001",
        "planning_id": "planning-001",
        "request_id": "request-001",
        "goal": "Complete Phase 8",
        "identity": user_identity,
        "steps": (build_step(),),
        "expected_outcomes": ("Planning completed",),
        "success_criteria": ("All tests pass",),
        "status": ProposalStatus.DRAFT,
        "confidence": 0.9,
    }

    values.update(overrides)

    return PlanProposal(**values)


# ============================================================================
# PlanningConfiguration
# ============================================================================


def test_planning_configuration_defaults() -> None:
    """Default configuration should be valid."""

    configuration = PlanningConfiguration()

    assert configuration.max_depth == 5
    assert configuration.time_budget_ms == 5000
    assert configuration.simulation_mode is False


@pytest.mark.parametrize(
    "depth",
    [
        1,
        5,
        10,
        25,
    ],
)
def test_planning_configuration_accepts_valid_depth(
    depth: int,
) -> None:
    configuration = PlanningConfiguration(
        max_depth=depth,
    )

    assert configuration.max_depth == depth


@pytest.mark.parametrize(
    "depth",
    [
        0,
        -1,
        -100,
    ],
)
def test_planning_configuration_rejects_invalid_depth(
    depth: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_depth must be greater than zero",
    ):
        PlanningConfiguration(
            max_depth=depth,
        )


@pytest.mark.parametrize(
    "depth",
    [
        True,
        3.5,
        "5",
    ],
)
def test_planning_configuration_rejects_invalid_depth_type(
    depth: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_depth must be an integer",
    ):
        PlanningConfiguration(
            max_depth=depth,  # type: ignore[arg-type]
        )


def test_planning_configuration_accepts_none_time_budget() -> None:
    configuration = PlanningConfiguration(
        time_budget_ms=None,
    )

    assert configuration.time_budget_ms is None


@pytest.mark.parametrize(
    "budget",
    [
        100,
        500,
        5000,
        30000,
    ],
)
def test_planning_configuration_accepts_valid_time_budget(
    budget: int,
) -> None:
    configuration = PlanningConfiguration(
        time_budget_ms=budget,
    )

    assert configuration.time_budget_ms == budget


@pytest.mark.parametrize(
    "budget",
    [
        0,
        50,
        99,
        -1,
    ],
)
def test_planning_configuration_rejects_invalid_time_budget(
    budget: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="time_budget_ms must be at least 100 milliseconds",
    ):
        PlanningConfiguration(
            time_budget_ms=budget,
        )


@pytest.mark.parametrize(
    "budget",
    [
        10.5,
        "5000",
        [],
    ],
)
def test_planning_configuration_rejects_invalid_time_budget_type(
    budget: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="time_budget_ms must be an integer or None",
    ):
        PlanningConfiguration(
            time_budget_ms=budget,  # type: ignore[arg-type]
        )


def test_planning_configuration_rejects_invalid_simulation_mode() -> None:
    with pytest.raises(
        TypeError,
        match="simulation_mode must be a boolean",
    ):
        PlanningConfiguration(
            simulation_mode="true",  # type: ignore[arg-type]
        )


def test_planning_configuration_to_dict_is_json_serializable() -> None:
    configuration = PlanningConfiguration()

    decoded = json.loads(
        json.dumps(
            configuration.to_dict(),
        )
    )

    assert decoded["max_depth"] == 5
    assert decoded["time_budget_ms"] == 5000
    assert decoded["simulation_mode"] is False


def test_planning_configuration_is_immutable() -> None:
    configuration = PlanningConfiguration()

    with pytest.raises(
        FrozenInstanceError,
    ):
        configuration.max_depth = 20  # type: ignore[misc]
