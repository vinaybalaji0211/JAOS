"""Public API and serialization tests for JAOS Intelligence."""

import json
from typing import Any

import jaos.intelligence as intelligence_api
import jaos.intelligence.context as context_api
import jaos.intelligence.exceptions as exceptions_api
import jaos.intelligence.interfaces as interfaces_api
import jaos.intelligence.models as models_api
import jaos.intelligence.prompt as prompt_api
from jaos.intelligence import (
    AgentAvailabilityState,
    AgentDescriptor,
    AgentHealthState,
    AgentResult,
    AgentTask,
    AgentTaskStatus,
    ContextBundle,
    ContextItem,
    ContextPolicy,
    ContextTrustLevel,
    ConversationRole,
    ConversationSession,
    ConversationSessionState,
    ConversationTurn,
    ExecutionProposal,
    FailureBehavior,
    IntelligenceApprovalRequiredError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceResult,
    IntelligenceResultStatus,
    IntelligenceScope,
    PlanningConfiguration,
    PlanningRequest,
    PlanProposal,
    ProposalStatus,
    ProposedPlanStep,
    ReasoningAssumption,
    ReasoningRequest,
    ReasoningResult,
    RiskLevel,
)


def build_serializable_models() -> tuple[Any, ...]:
    """Build a representative instance of every public domain model."""

    identity = IntelligenceIdentity(
        scope=IntelligenceScope.USER,
        identity_id="vinay",
    )

    request = IntelligenceRequest(
        objective="Explain the JAOS architecture",
        request_type=IntelligenceRequestType.REASONING,
        identity=identity,
        session_id="session-001",
    )

    result = IntelligenceResult(
        request_id=request.request_id,
        status=IntelligenceResultStatus.SUCCEEDED,
        output="JAOS is a modular artificial operating system.",
        confidence=0.9,
    )

    turn = ConversationTurn(
        session_id="session-001",
        role=ConversationRole.USER,
        content="Explain the JAOS architecture",
        source="cli",
    )

    session = ConversationSession(
        identity=identity,
        session_id="session-001",
        state=ConversationSessionState.ACTIVE,
        turns=(turn,),
    )

    context_item = ContextItem(
        context_type=IntelligenceContextType.USER,
        content="The user is developing JAOS.",
        identity=identity,
        source="conversation",
        trust_level=ContextTrustLevel.USER_PROVIDED,
        estimated_tokens=8,
    )

    context_bundle = ContextBundle(
        request_id=request.request_id,
        identity=identity,
        items=(context_item,),
        max_tokens=100,
    )

    assumption = ReasoningAssumption(
        statement="The user wants a technical overview.",
        confidence=0.8,
        source_context_ids=(context_item.item_id,),
    )

    reasoning_request = ReasoningRequest(
        request_id=request.request_id,
        objective=request.objective,
        context_bundle=context_bundle,
    )

    reasoning_result = ReasoningResult(
        request_id=request.request_id,
        objective_interpretation="Produce a JAOS platform overview.",
        reasoning_summary="Use approved architecture context.",
        confidence=0.9,
        assumptions=(assumption,),
        recommended_next_action="Return the architecture overview.",
    )

    plan_step = ProposedPlanStep(
        description="Collect approved JAOS architecture context",
        step_order=1,
        required_capability="knowledge.search",
        expected_output="Relevant architecture context",
        success_condition="Approved context is available",
        permission_requirements=("memory.read",),
        risk_level=RiskLevel.LOW,
        failure_behavior=FailureBehavior.STOP,
    )

    planning_request = PlanningRequest(
        request_id=request.request_id,
        planning_id="planning-001",
        goal="Produce a JAOS platform overview",
        identity=identity,
        reasoning_result=reasoning_result,
        configuration=PlanningConfiguration(),
        success_criteria=("The response is accurate and structured",),
    )

    plan_proposal = PlanProposal(
        planning_id=planning_request.planning_id,
        request_id=request.request_id,
        goal=planning_request.goal,
        identity=identity,
        steps=(plan_step,),
        expected_outcomes=("JAOS architecture is explained",),
        success_criteria=("The response is accurate and structured",),
        confidence=0.9,
    )

    agent_descriptor = AgentDescriptor(
        agent_id="research-agent",
        name="Research Agent",
        capabilities=("knowledge.search",),
        input_contracts=("agent.task",),
        output_contracts=("agent.result",),
        required_permissions=("memory.read",),
        availability_state=AgentAvailabilityState.AVAILABLE,
        health_state=AgentHealthState.HEALTHY,
        max_delegation_depth=1,
    )

    agent_task = AgentTask(
        parent_request_id=request.request_id,
        target_capability="knowledge.search",
        identity=identity,
        task_input={"query": "JAOS architecture"},
        agent_id=agent_descriptor.agent_id,
        status=AgentTaskStatus.ROUTED,
        permission_scope=("memory.read",),
        max_delegation_depth=1,
    )

    agent_result = AgentResult(
        task_id=agent_task.task_id,
        agent_id=agent_descriptor.agent_id,
        status=AgentTaskStatus.SUCCEEDED,
        output="Architecture context collected",
        structured_output={"matches": 1},
        confidence=0.9,
    )

    execution_proposal = ExecutionProposal(
        source_request_id=request.request_id,
        plan_proposal_id=plan_proposal.proposal_id,
        agent_task_id=agent_task.task_id,
        action_description="Search approved JAOS knowledge",
        required_capability="knowledge.search",
        identity=identity,
        structured_inputs={"query": "JAOS architecture"},
        suggested_tool_category="knowledge.search",
        expected_result="Relevant architecture context",
        success_criteria=("Approved context is returned",),
        permission_requirements=("memory.read",),
        risk_level=RiskLevel.LOW,
        recovery_guidance=("Return a structured failure result",),
        status=ProposalStatus.VALIDATED,
    )

    return (
        identity,
        request,
        result,
        turn,
        session,
        context_item,
        context_bundle,
        assumption,
        reasoning_request,
        reasoning_result,
        plan_step,
        planning_request,
        plan_proposal,
        agent_descriptor,
        agent_task,
        agent_result,
        execution_proposal,
    )


def test_public_exports_are_unique_and_ordered() -> None:
    """Verify the Intelligence Platform public API contract."""

    assert len(intelligence_api.__all__) == 85

    assert len(intelligence_api.__all__) == len(set(intelligence_api.__all__))

    assert intelligence_api.__all__ == sorted(intelligence_api.__all__)


def test_all_public_exports_are_accessible() -> None:
    """Every public export must exist."""

    for export_name in intelligence_api.__all__:
        assert hasattr(
            intelligence_api,
            export_name,
        )


def test_public_api_matches_package_exports() -> None:
    """The package exports should equal the union of subpackages."""

    package_exports = (
        set(models_api.__all__)
        | set(exceptions_api.__all__)
        | set(interfaces_api.__all__)
        | set(context_api.__all__)
        | set(prompt_api.__all__)
    )

    assert set(intelligence_api.__all__) == package_exports


def test_package_export_counts() -> None:
    """Verify each public package exposes the expected symbols."""

    assert len(models_api.__all__) == 31
    assert len(exceptions_api.__all__) == 12
    assert len(interfaces_api.__all__) == 10
    assert len(context_api.__all__) == 18
    assert len(prompt_api.__all__) == 14


def test_domain_models_are_json_serializable() -> None:
    """Every representative model should serialize cleanly."""

    for model in build_serializable_models():
        serialized = model.to_dict()

        encoded = json.dumps(
            serialized,
            sort_keys=True,
        )

        assert isinstance(
            serialized,
            dict,
        )

        assert isinstance(
            encoded,
            str,
        )

        assert encoded


def test_context_policy_is_json_serializable() -> None:
    """ContextPolicy should serialize deterministically."""

    policy = ContextPolicy(
        max_tokens=1024,
        max_items=20,
        minimum_relevance=0.25,
    )

    encoded = json.dumps(
        policy.to_dict(),
        sort_keys=True,
    )

    decoded = json.loads(encoded)

    assert decoded["max_tokens"] == 1024
    assert decoded["max_items"] == 20
    assert decoded["minimum_relevance"] == 0.25


def test_enum_values_are_json_serializable() -> None:
    """All public enums should serialize using their values."""

    enum_types = (
        AgentAvailabilityState,
        AgentHealthState,
        AgentTaskStatus,
        ContextTrustLevel,
        ConversationRole,
        ConversationSessionState,
        IntelligenceContextType,
        IntelligenceRequestType,
        IntelligenceResultStatus,
        IntelligenceScope,
        ProposalStatus,
        RiskLevel,
    )

    values = [member.value for enum_type in enum_types for member in enum_type]

    assert json.loads(json.dumps(values)) == values


def test_structured_errors_are_json_serializable() -> None:
    """Structured Intelligence exceptions must serialize correctly."""

    error = IntelligenceApprovalRequiredError(
        "Approval required",
        request_id="request-001",
        details={"permission": "memory.write"},
    )

    encoded = json.dumps(
        error.to_dict(),
        sort_keys=True,
    )

    decoded = json.loads(encoded)

    assert decoded["error_code"] == "intelligence_approval_required"

    assert decoded["request_id"] == "request-001"

    assert decoded["details"] == {
        "permission": "memory.write",
    }


def test_every_public_model_supports_to_dict() -> None:
    """Every representative public model should expose to_dict()."""

    for model in build_serializable_models():

        assert hasattr(
            model,
            "to_dict",
        )

        serialized = model.to_dict()

        assert isinstance(
            serialized,
            dict,
        )


def test_public_api_contains_new_planning_exports() -> None:
    """Verify recently-added planning exports remain public."""

    assert "FailureBehavior" in intelligence_api.__all__

    assert "PlanningConfiguration" in intelligence_api.__all__


def test_public_api_exports_are_sorted() -> None:
    """Public exports must remain alphabetically ordered."""

    exports = intelligence_api.__all__

    assert exports == sorted(exports)


def test_public_api_exports_are_unique() -> None:
    """Public exports must not contain duplicates."""

    exports = intelligence_api.__all__

    assert len(exports) == len(set(exports))
