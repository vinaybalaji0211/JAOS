"""Tests for JAOS agent and execution proposal models."""

from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    AgentAvailabilityState,
    AgentDescriptor,
    AgentHealthState,
    AgentResult,
    AgentTask,
    AgentTaskStatus,
    ExecutionProposal,
    IntelligenceIdentity,
    IntelligenceScope,
    ProposalStatus,
    RiskLevel,
)


def create_identity() -> IntelligenceIdentity:
    """Create a reusable test identity."""

    return IntelligenceIdentity(
        scope=IntelligenceScope.USER,
        identity_id="vinay",
    )


def create_descriptor(**overrides: object) -> AgentDescriptor:
    """Create an agent descriptor with valid defaults."""

    values = {
        "agent_id": "research-agent",
        "name": "Research Agent",
        "capabilities": ("knowledge.search", "context.analysis"),
        "input_contracts": ("intelligence.request",),
        "output_contracts": ("intelligence.result",),
        "required_permissions": ("memory.read",),
        "availability_state": AgentAvailabilityState.AVAILABLE,
        "health_state": AgentHealthState.HEALTHY,
        "max_delegation_depth": 2,
        "metadata": {"owner": "jaos"},
    }
    values.update(overrides)
    return AgentDescriptor(**values)


def create_task(**overrides: object) -> AgentTask:
    """Create an agent task with valid defaults."""

    values = {
        "parent_request_id": "request-001",
        "target_capability": "knowledge.search",
        "identity": create_identity(),
        "task_input": {"query": "JAOS architecture"},
        "context_source_ids": ("context-001",),
        "permission_scope": ("memory.read",),
        "resource_limit_seconds": 30.0,
        "delegation_depth": 0,
        "max_delegation_depth": 2,
        "metadata": {"source": "test"},
    }
    values.update(overrides)
    return AgentTask(**values)


def create_execution_proposal(
    **overrides: object,
) -> ExecutionProposal:
    """Create an execution proposal with valid defaults."""

    values = {
        "source_request_id": "request-001",
        "action_description": "Search approved project knowledge",
        "required_capability": "knowledge.search",
        "identity": create_identity(),
        "structured_inputs": {"query": "JAOS architecture"},
        "expected_result": "Relevant project knowledge",
        "success_criteria": ("Relevant results are returned",),
        "suggested_tool_category": "Knowledge Search",
        "permission_requirements": ("memory.read",),
        "risk_level": RiskLevel.LOW,
        "recovery_guidance": ("Return a structured failure result",),
        "status": ProposalStatus.VALIDATED,
        "metadata": {"source": "planning"},
    }
    values.update(overrides)
    return ExecutionProposal(**values)


def test_agent_descriptor_creation() -> None:
    descriptor = create_descriptor()

    assert descriptor.agent_id == "research-agent"
    assert descriptor.name == "Research Agent"
    assert descriptor.availability_state is AgentAvailabilityState.AVAILABLE
    assert descriptor.health_state is AgentHealthState.HEALTHY
    assert descriptor.max_delegation_depth == 2


@pytest.mark.parametrize(
    "field_name",
    ["agent_id", "name"],
)
def test_agent_descriptor_requires_text_fields(field_name: str) -> None:
    with pytest.raises(ValueError):
        create_descriptor(**{field_name: "   "})


@pytest.mark.parametrize(
    "field_name",
    ["capabilities", "input_contracts", "output_contracts"],
)
def test_agent_descriptor_requires_contract_collections(
    field_name: str,
) -> None:
    with pytest.raises(ValueError):
        create_descriptor(**{field_name: ()})


def test_agent_descriptor_normalizes_and_deduplicates_values() -> None:
    descriptor = create_descriptor(
        capabilities=(" Knowledge.Search ", "knowledge.search"),
        required_permissions=(" Memory.Read ", "memory.read"),
    )

    assert descriptor.capabilities == ("knowledge.search",)
    assert descriptor.required_permissions == ("memory.read",)


def test_agent_descriptor_rejects_invalid_availability_state() -> None:
    with pytest.raises(TypeError):
        create_descriptor(availability_state="available")


def test_agent_descriptor_rejects_invalid_health_state() -> None:
    with pytest.raises(TypeError):
        create_descriptor(health_state="healthy")


def test_agent_descriptor_rejects_negative_delegation_depth() -> None:
    with pytest.raises(ValueError):
        create_descriptor(max_delegation_depth=-1)


def test_agent_descriptor_serialization() -> None:
    descriptor = create_descriptor()
    serialized = descriptor.to_dict()

    assert serialized["agent_id"] == descriptor.agent_id
    assert serialized["capabilities"] == list(descriptor.capabilities)
    assert serialized["availability_state"] == "available"
    assert serialized["health_state"] == "healthy"
    assert serialized["metadata"] == {"owner": "jaos"}


def test_agent_task_creation() -> None:
    task = create_task()

    assert task.parent_request_id == "request-001"
    assert task.target_capability == "knowledge.search"
    assert task.identity == create_identity()
    assert task.status is AgentTaskStatus.PENDING
    assert task.agent_id is None


def test_agent_task_normalizes_capability_and_permissions() -> None:
    task = create_task(
        target_capability=" Knowledge.Search ",
        permission_scope=(" Memory.Read ", "memory.read"),
    )

    assert task.target_capability == "knowledge.search"
    assert task.permission_scope == ("memory.read",)


@pytest.mark.parametrize(
    "status",
    [AgentTaskStatus.ROUTED, AgentTaskStatus.RUNNING],
)
def test_routed_agent_task_requires_agent_id(
    status: AgentTaskStatus,
) -> None:
    with pytest.raises(ValueError):
        create_task(status=status, agent_id=None)


@pytest.mark.parametrize(
    "status",
    [AgentTaskStatus.ROUTED, AgentTaskStatus.RUNNING],
)
def test_routed_agent_task_accepts_agent_id(
    status: AgentTaskStatus,
) -> None:
    task = create_task(
        status=status,
        agent_id="research-agent",
    )

    assert task.agent_id == "research-agent"
    assert task.status is status


def test_agent_task_rejects_past_deadline() -> None:
    with pytest.raises(ValueError):
        create_task(
            deadline_at=datetime.now(timezone.utc) - timedelta(seconds=1)
        )


def test_agent_task_normalizes_deadline_to_utc() -> None:
    deadline = datetime.now(timezone.utc) + timedelta(minutes=5)
    task = create_task(deadline_at=deadline)

    assert task.deadline_at is not None
    assert task.deadline_at.tzinfo == timezone.utc


@pytest.mark.parametrize("resource_limit", [0, -1])
def test_agent_task_requires_positive_resource_limit(
    resource_limit: float,
) -> None:
    with pytest.raises(ValueError):
        create_task(resource_limit_seconds=resource_limit)


@pytest.mark.parametrize(
    ("delegation_depth", "max_delegation_depth"),
    [
        (-1, 2),
        (0, -1),
        (3, 2),
    ],
)
def test_agent_task_validates_delegation_depth(
    delegation_depth: int,
    max_delegation_depth: int,
) -> None:
    with pytest.raises(ValueError):
        create_task(
            delegation_depth=delegation_depth,
            max_delegation_depth=max_delegation_depth,
        )


def test_agent_task_serialization() -> None:
    task = create_task(
        agent_id="research-agent",
        status=AgentTaskStatus.ROUTED,
    )
    serialized = task.to_dict()

    assert serialized["task_id"] == task.task_id
    assert serialized["parent_request_id"] == "request-001"
    assert serialized["agent_id"] == "research-agent"
    assert serialized["status"] == "routed"
    assert serialized["identity"] == create_identity().to_dict()
    assert serialized["permission_scope"] == ["memory.read"]


def test_agent_result_success_with_text_output() -> None:
    result = AgentResult(
        task_id="task-001",
        agent_id="research-agent",
        status=AgentTaskStatus.SUCCEEDED,
        output="Search completed",
        confidence=0.9,
    )

    assert result.status is AgentTaskStatus.SUCCEEDED
    assert result.output == "Search completed"
    assert result.confidence == 0.9


def test_agent_result_success_with_structured_output() -> None:
    result = AgentResult(
        task_id="task-001",
        agent_id="research-agent",
        status=AgentTaskStatus.SUCCEEDED,
        structured_output={"matches": 3},
    )

    assert result.structured_output == {"matches": 3}


@pytest.mark.parametrize(
    "status",
    [
        AgentTaskStatus.FAILED,
        AgentTaskStatus.REJECTED,
        AgentTaskStatus.CANCELLED,
    ],
)
def test_agent_result_supports_terminal_failure_statuses(
    status: AgentTaskStatus,
) -> None:
    result = AgentResult(
        task_id="task-001",
        agent_id="research-agent",
        status=status,
        error_message="Task did not complete",
    )

    assert result.status is status
    assert result.error_message == "Task did not complete"


@pytest.mark.parametrize(
    "status",
    [
        AgentTaskStatus.PENDING,
        AgentTaskStatus.ROUTED,
        AgentTaskStatus.RUNNING,
    ],
)
def test_agent_result_rejects_non_terminal_status(
    status: AgentTaskStatus,
) -> None:
    with pytest.raises(ValueError):
        AgentResult(
            task_id="task-001",
            agent_id="research-agent",
            status=status,
            output="Incomplete result",
        )


def test_successful_agent_result_requires_output() -> None:
    with pytest.raises(ValueError):
        AgentResult(
            task_id="task-001",
            agent_id="research-agent",
            status=AgentTaskStatus.SUCCEEDED,
        )


@pytest.mark.parametrize(
    "status",
    [
        AgentTaskStatus.FAILED,
        AgentTaskStatus.REJECTED,
        AgentTaskStatus.CANCELLED,
    ],
)
def test_unsuccessful_agent_result_requires_error_message(
    status: AgentTaskStatus,
) -> None:
    with pytest.raises(ValueError):
        AgentResult(
            task_id="task-001",
            agent_id="research-agent",
            status=status,
        )


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_agent_result_validates_confidence(confidence: float) -> None:
    with pytest.raises(ValueError):
        AgentResult(
            task_id="task-001",
            agent_id="research-agent",
            status=AgentTaskStatus.SUCCEEDED,
            output="Completed",
            confidence=confidence,
        )


def test_agent_result_serialization() -> None:
    result = AgentResult(
        task_id="task-001",
        agent_id="research-agent",
        status=AgentTaskStatus.SUCCEEDED,
        output="Completed",
        structured_output={"matches": 2},
        confidence=0.8,
        metadata={"provider": "internal"},
    )
    serialized = result.to_dict()

    assert serialized["result_id"] == result.result_id
    assert serialized["task_id"] == "task-001"
    assert serialized["status"] == "succeeded"
    assert serialized["structured_output"] == {"matches": 2}
    assert serialized["confidence"] == 0.8
    assert serialized["completed_at"].endswith("+00:00")


def test_execution_proposal_creation() -> None:
    proposal = create_execution_proposal()

    assert proposal.source_request_id == "request-001"
    assert proposal.required_capability == "knowledge.search"
    assert proposal.status is ProposalStatus.VALIDATED
    assert proposal.risk_level is RiskLevel.LOW


def test_execution_proposal_normalizes_collections() -> None:
    proposal = create_execution_proposal(
        required_capability=" Knowledge.Search ",
        success_criteria=(" Result Returned ", "Result Returned"),
        permission_requirements=(" Memory.Read ", "memory.read"),
        suggested_tool_category=" Knowledge Search ",
    )

    assert proposal.required_capability == "knowledge.search"
    assert proposal.success_criteria == ("Result Returned",)
    assert proposal.permission_requirements == ("memory.read",)
    assert proposal.suggested_tool_category == "knowledge search"


def test_execution_proposal_requires_success_criteria() -> None:
    with pytest.raises(ValueError):
        create_execution_proposal(success_criteria=())


def test_execution_proposal_requires_identity() -> None:
    with pytest.raises(TypeError):
        create_execution_proposal(identity="vinay")


def test_execution_proposal_requires_structured_inputs_dictionary() -> None:
    with pytest.raises(TypeError):
        create_execution_proposal(structured_inputs=("query", "value"))


def test_execution_proposal_rejects_invalid_risk_level() -> None:
    with pytest.raises(TypeError):
        create_execution_proposal(risk_level="low")


def test_execution_proposal_rejects_invalid_status() -> None:
    with pytest.raises(TypeError):
        create_execution_proposal(status="validated")


def test_execution_proposal_requires_aware_created_at() -> None:
    with pytest.raises(ValueError):
        create_execution_proposal(created_at=datetime.now())


def test_execution_proposal_serialization() -> None:
    proposal = create_execution_proposal(
        plan_proposal_id="plan-001",
        agent_task_id="task-001",
    )
    serialized = proposal.to_dict()

    assert serialized["proposal_id"] == proposal.proposal_id
    assert serialized["source_request_id"] == "request-001"
    assert serialized["plan_proposal_id"] == "plan-001"
    assert serialized["agent_task_id"] == "task-001"
    assert serialized["identity"] == create_identity().to_dict()
    assert serialized["status"] == "validated"
    assert serialized["risk_level"] == "low"
    assert serialized["permission_requirements"] == ["memory.read"]
    assert serialized["created_at"].endswith("+00:00")