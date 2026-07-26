"""Tests for AI Intelligence Platform planning models."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from jaos.intelligence import (
    ContextBundle,
    IntelligenceIdentity,
    IntelligenceScope,
    PlanProposal,
    PlanningRequest,
    ProposalStatus,
    ProposedPlanStep,
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


@pytest.fixture
def reasoning_result() -> ReasoningResult:
    return ReasoningResult(
        request_id="request-001",
        objective_interpretation="Continue Phase 8",
        reasoning_summary="Complete model contracts first",
        confidence=0.9,
        result_id="reasoning-result-001",
    )


def build_step(**overrides: object) -> ProposedPlanStep:
    arguments: dict[str, object] = {
        "description": "Create intelligence models",
        "step_order": 1,
        "required_capability": "coding",
        "expected_output": "Validated model files",
        "success_condition": "All unit tests pass",
        "step_id": "step-001",
    }
    arguments.update(overrides)

    return ProposedPlanStep(**arguments)  # type: ignore[arg-type]


def test_proposed_step_normalizes_valid_input() -> None:
    metadata = {"owner": "jaos"}

    step = ProposedPlanStep(
        description=" Create intelligence models ",
        step_order=1,
        required_capability=" CODING ",
        expected_output=" Validated model files ",
        success_condition=" All unit tests pass ",
        step_id=" step-001 ",
        dependencies=(" dependency-001 ", "dependency-001"),
        suggested_tool_category=" FILESYSTEM ",
        input_references=(" requirement-001 ",),
        permission_requirements=(" Read ", "read", " Write "),
        risk_level=RiskLevel.LOW,
        failure_behavior=" STOP ",
        metadata=metadata,
    )

    metadata["owner"] = "changed"

    assert step.step_id == "step-001"
    assert step.description == "Create intelligence models"
    assert step.required_capability == "coding"
    assert step.dependencies == ("dependency-001",)
    assert step.suggested_tool_category == "filesystem"
    assert step.input_references == ("requirement-001",)
    assert step.permission_requirements == ("read", "write")
    assert step.failure_behavior == "stop"
    assert step.metadata == {"owner": "jaos"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("step_id", ""),
        ("description", "   "),
        ("required_capability", ""),
        ("expected_output", "   "),
        ("success_condition", ""),
        ("failure_behavior", "   "),
    ],
)
def test_proposed_step_rejects_invalid_required_string(
    field_name: str,
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        build_step(**{field_name: value})


@pytest.mark.parametrize("step_order", [True, 1.5])
def test_proposed_step_rejects_invalid_order_type(
    step_order: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="step_order must be an integer",
    ):
        build_step(step_order=step_order)


@pytest.mark.parametrize("step_order", [0, -1])
def test_proposed_step_rejects_non_positive_order(
    step_order: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="step_order must be greater than zero",
    ):
        build_step(step_order=step_order)


def test_proposed_step_rejects_invalid_tool_category() -> None:
    with pytest.raises(
        TypeError,
        match="suggested_tool_category must be a string or None",
    ):
        build_step(suggested_tool_category=123)


def test_proposed_step_rejects_invalid_risk_level() -> None:
    with pytest.raises(
        TypeError,
        match="risk_level must be an instance of RiskLevel",
    ):
        build_step(risk_level="low")


def test_proposed_step_rejects_self_dependency() -> None:
    with pytest.raises(
        ValueError,
        match="cannot depend on itself",
    ):
        build_step(dependencies=("step-001",))


def test_proposed_step_rejects_string_dependency_collection() -> None:
    with pytest.raises(
        TypeError,
        match="dependencies must be a collection",
    ):
        build_step(dependencies="step-000")


def test_proposed_step_rejects_empty_permission() -> None:
    with pytest.raises(
        ValueError,
        match="permission_requirements must contain only",
    ):
        build_step(permission_requirements=("read", "   "))


def test_proposed_step_rejects_invalid_metadata() -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        build_step(metadata=[])


def test_proposed_step_to_dict_is_json_serializable() -> None:
    step = build_step(
        permission_requirements=("write",),
        risk_level=RiskLevel.MEDIUM,
    )

    decoded = json.loads(json.dumps(step.to_dict()))

    assert decoded["step_id"] == "step-001"
    assert decoded["step_order"] == 1
    assert decoded["required_capability"] == "coding"
    assert decoded["permission_requirements"] == ["write"]
    assert decoded["risk_level"] == "medium"


def test_proposed_step_is_immutable() -> None:
    step = build_step()

    with pytest.raises(FrozenInstanceError):
        step.description = "Changed"  # type: ignore[misc]


def test_planning_request_normalizes_valid_input(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
    reasoning_result: ReasoningResult,
) -> None:
    metadata = {"source": "reasoning"}

    request = PlanningRequest(
        request_id=" request-001 ",
        goal=" Complete Phase 8 models ",
        identity=user_identity,
        reasoning_result=reasoning_result,
        context_bundle=context_bundle,
        planning_id=" planning-001 ",
        constraints=(" Preserve APIs ", "Preserve APIs"),
        available_capabilities=(" Coding ", "coding", " Testing "),
        permission_constraints=(" Read ", "write"),
        risk_policy=" SAFE ",
        success_criteria=("All tests pass",),
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert request.request_id == "request-001"
    assert request.planning_id == "planning-001"
    assert request.goal == "Complete Phase 8 models"
    assert request.constraints == ("Preserve APIs",)
    assert request.available_capabilities == ("coding", "testing")
    assert request.permission_constraints == ("read", "write")
    assert request.risk_policy == "safe"
    assert request.metadata == {"source": "reasoning"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("planning_id", ""),
        ("request_id", "   "),
        ("goal", ""),
        ("risk_policy", "   "),
    ],
)
def test_planning_request_rejects_invalid_required_string(
    field_name: str,
    value: str,
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    arguments: dict[str, object] = {
        "request_id": "request-001",
        "goal": "Complete Phase 8",
        "identity": user_identity,
        "context_bundle": context_bundle,
        "planning_id": "planning-001",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        PlanningRequest(**arguments)  # type: ignore[arg-type]


def test_planning_request_requires_reasoning_or_context(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="requires reasoning_result or context_bundle",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
        )


def test_planning_request_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an instance",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity="vinay",  # type: ignore[arg-type]
            context_bundle=None,
            reasoning_result=ReasoningResult(
                request_id="request-001",
                objective_interpretation="Continue",
                reasoning_summary="Complete contracts",
                confidence=0.9,
            ),
        )


def test_planning_request_rejects_invalid_reasoning_result(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="reasoning_result must be a ReasoningResult or None",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            reasoning_result={},  # type: ignore[arg-type]
        )


def test_planning_request_rejects_invalid_context_bundle(
    user_identity: IntelligenceIdentity,
    reasoning_result: ReasoningResult,
) -> None:
    with pytest.raises(
        TypeError,
        match="context_bundle must be a ContextBundle or None",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            reasoning_result=reasoning_result,
            context_bundle={},  # type: ignore[arg-type]
        )


def test_planning_request_rejects_reasoning_request_mismatch(
    user_identity: IntelligenceIdentity,
) -> None:
    reasoning = ReasoningResult(
        request_id="another-request",
        objective_interpretation="Continue",
        reasoning_summary="Complete contracts",
        confidence=0.9,
    )

    with pytest.raises(
        ValueError,
        match="reasoning_result request_id must match request_id",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            reasoning_result=reasoning,
        )


def test_planning_request_rejects_context_request_mismatch(
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
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=bundle,
        )


def test_planning_request_rejects_context_identity_mismatch(
    user_identity: IntelligenceIdentity,
) -> None:
    project_identity = IntelligenceIdentity(
        IntelligenceScope.PROJECT,
        "jaos",
    )
    bundle = ContextBundle(
        request_id="request-001",
        identity=project_identity,
    )

    with pytest.raises(
        ValueError,
        match="context_bundle identity must match identity",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=bundle,
        )


def test_planning_request_rejects_string_capability_collection(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        TypeError,
        match="available_capabilities must be a collection",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=context_bundle,
            available_capabilities="coding",  # type: ignore[arg-type]
        )


def test_planning_request_rejects_empty_success_criterion(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        ValueError,
        match="success_criteria must contain only",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=context_bundle,
            success_criteria=("All tests pass", "   "),
        )


def test_planning_request_rejects_invalid_metadata(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=context_bundle,
            metadata=[],  # type: ignore[arg-type]
        )


def test_planning_request_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        PlanningRequest(
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            context_bundle=context_bundle,
            created_at=datetime(2026, 1, 1),
        )


def test_planning_request_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
    reasoning_result: ReasoningResult,
) -> None:
    request = PlanningRequest(
        request_id="request-001",
        goal="Complete Phase 8",
        identity=user_identity,
        reasoning_result=reasoning_result,
        context_bundle=context_bundle,
        planning_id="planning-001",
        success_criteria=("All tests pass",),
    )

    decoded = json.loads(json.dumps(request.to_dict()))

    assert decoded["planning_id"] == "planning-001"
    assert decoded["request_id"] == "request-001"
    assert decoded["identity"]["identity_id"] == "vinay"
    assert decoded["reasoning_result"]["request_id"] == "request-001"
    assert decoded["context_bundle"]["bundle_id"] == "bundle-001"


def test_planning_request_is_immutable(
    user_identity: IntelligenceIdentity,
    context_bundle: ContextBundle,
) -> None:
    request = PlanningRequest(
        request_id="request-001",
        goal="Complete Phase 8",
        identity=user_identity,
        context_bundle=context_bundle,
    )

    with pytest.raises(FrozenInstanceError):
        request.goal = "Changed"  # type: ignore[misc]


def test_plan_proposal_normalizes_and_derives_step_requirements(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_step(
        step_id="step-001",
        step_order=1,
        required_capability="coding",
        permission_requirements=("read",),
        risk_level=RiskLevel.LOW,
    )
    second = build_step(
        step_id="step-002",
        step_order=2,
        description="Run tests",
        required_capability="testing",
        dependencies=("step-001",),
        permission_requirements=("execute",),
        risk_level=RiskLevel.HIGH,
    )
    metadata = {"source": "planning-engine"}

    proposal = PlanProposal(
        planning_id=" planning-001 ",
        request_id=" request-001 ",
        goal=" Complete Phase 8 ",
        identity=user_identity,
        steps=[first, second],  # type: ignore[arg-type]
        expected_outcomes=(" Models complete ",),
        success_criteria=(" All tests pass ",),
        proposal_id=" proposal-001 ",
        reasoning_result_id=" reasoning-result-001 ",
        required_capabilities=(" Review ",),
        permission_requirements=(" Approve ",),
        failure_conditions=("Test failure",),
        recovery_guidance=("Fix failing tests",),
        risks=("Regression risk",),
        confidence=0.9,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert proposal.proposal_id == "proposal-001"
    assert proposal.planning_id == "planning-001"
    assert proposal.request_id == "request-001"
    assert proposal.goal == "Complete Phase 8"
    assert proposal.steps == (first, second)
    assert proposal.required_capabilities == (
        "review",
        "coding",
        "testing",
    )
    assert proposal.permission_requirements == (
        "approve",
        "read",
        "execute",
    )
    assert proposal.risk_level is RiskLevel.HIGH
    assert proposal.reasoning_result_id == "reasoning-result-001"
    assert proposal.metadata == {"source": "planning-engine"}


def test_plan_proposal_requires_at_least_one_step(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="must contain at least one step",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_invalid_step_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="steps must contain only ProposedPlanStep instances",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=("invalid",),  # type: ignore[arg-type]
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_duplicate_step_ids(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_step(step_id="step-001", step_order=1)
    second = build_step(step_id="step-001", step_order=2)

    with pytest.raises(
        ValueError,
        match="proposed step IDs must be unique",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(first, second),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_non_consecutive_order(
    user_identity: IntelligenceIdentity,
) -> None:
    step = build_step(step_order=2)

    with pytest.raises(
        ValueError,
        match="ordered consecutively from one",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(step,),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_unknown_dependency(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_step(step_id="step-001", step_order=1)
    second = build_step(
        step_id="step-002",
        step_order=2,
        dependencies=("unknown",),
    )

    with pytest.raises(
        ValueError,
        match="dependencies must reference proposal steps",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(first, second),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_dependency_on_later_step(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_step(
        step_id="step-001",
        step_order=1,
        dependencies=("step-002",),
    )
    second = build_step(step_id="step-002", step_order=2)

    with pytest.raises(
        ValueError,
        match="dependencies must reference earlier steps",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(first, second),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_rejects_invalid_status(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="status must be an instance of ProposalStatus",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
            status="draft",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("confidence", [True, "0.9"])
def test_plan_proposal_rejects_invalid_confidence_type(
    confidence: object,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="confidence must be a number",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
            confidence=confidence,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_plan_proposal_rejects_invalid_confidence_value(
    confidence: float,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="confidence must be between",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
            confidence=confidence,
        )


def test_plan_proposal_requires_expected_outcome(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="expected_outcomes must contain at least one value",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=(),
            success_criteria=("All tests pass",),
        )


def test_plan_proposal_requires_success_criterion(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="success_criteria must contain at least one value",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=("Models complete",),
            success_criteria=(),
        )


def test_plan_proposal_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        PlanProposal(
            planning_id="planning-001",
            request_id="request-001",
            goal="Complete Phase 8",
            identity=user_identity,
            steps=(build_step(),),
            expected_outcomes=("Models complete",),
            success_criteria=("All tests pass",),
            created_at=datetime(2026, 1, 1),
        )


def test_plan_proposal_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
) -> None:
    proposal = PlanProposal(
        planning_id="planning-001",
        request_id="request-001",
        goal="Complete Phase 8",
        identity=user_identity,
        steps=(build_step(),),
        expected_outcomes=("Models complete",),
        success_criteria=("All tests pass",),
        proposal_id="proposal-001",
        confidence=0.9,
    )

    decoded = json.loads(json.dumps(proposal.to_dict()))

    assert decoded["proposal_id"] == "proposal-001"
    assert decoded["planning_id"] == "planning-001"
    assert decoded["status"] == "draft"
    assert decoded["steps"][0]["step_id"] == "step-001"
    assert decoded["required_capabilities"] == ["coding"]


def test_plan_proposal_is_immutable(
    user_identity: IntelligenceIdentity,
) -> None:
    proposal = PlanProposal(
        planning_id="planning-001",
        request_id="request-001",
        goal="Complete Phase 8",
        identity=user_identity,
        steps=(build_step(),),
        expected_outcomes=("Models complete",),
        success_criteria=("All tests pass",),
    )

    with pytest.raises(FrozenInstanceError):
        proposal.status = ProposalStatus.APPROVED  # type: ignore[misc]