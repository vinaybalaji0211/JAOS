"""Public models for the JAOS AI Intelligence Platform.

Models are resolved lazily so importing completed conversation models does not
eagerly import paused planning, reasoning, agent, or execution-proposal models.
"""

from importlib import import_module

_EXPORT_MODULES = {
    "AgentAvailabilityState": (
        "jaos.intelligence.models.agent_availability_state"
    ),
    "AgentDescriptor": "jaos.intelligence.models.agent_descriptor",
    "AgentHealthState": "jaos.intelligence.models.agent_health_state",
    "AgentResult": "jaos.intelligence.models.agent_result",
    "AgentTask": "jaos.intelligence.models.agent_task",
    "AgentTaskStatus": "jaos.intelligence.models.agent_task_status",
    "ContextBundle": "jaos.intelligence.models.context_bundle",
    "ContextItem": "jaos.intelligence.models.context_item",
    "ContextTrustLevel": "jaos.intelligence.models.context_trust_level",
    "ConversationRole": "jaos.intelligence.models.conversation_role",
    "ConversationSession": "jaos.intelligence.models.conversation_session",
    "ConversationSessionState": (
        "jaos.intelligence.models.conversation_session_state"
    ),
    "ConversationTurn": "jaos.intelligence.models.conversation_turn",
    "ExecutionProposal": "jaos.intelligence.models.execution_proposal",
    "FailureBehavior": "jaos.intelligence.models.failure_behavior",
    "IntelligenceContextType": (
        "jaos.intelligence.models.intelligence_context_type"
    ),
    "IntelligenceIdentity": "jaos.intelligence.models.intelligence_identity",
    "IntelligenceRequest": "jaos.intelligence.models.intelligence_request",
    "IntelligenceRequestType": (
        "jaos.intelligence.models.intelligence_request_type"
    ),
    "IntelligenceResult": "jaos.intelligence.models.intelligence_result",
    "IntelligenceResultStatus": (
        "jaos.intelligence.models.intelligence_result_status"
    ),
    "IntelligenceScope": "jaos.intelligence.models.intelligence_scope",
    "PlanProposal": "jaos.intelligence.models.plan_proposal",
    "PlanningConfiguration": (
        "jaos.intelligence.models.planning_configuration"
    ),
    "PlanningRequest": "jaos.intelligence.models.planning_request",
    "ProposalStatus": "jaos.intelligence.models.proposal_status",
    "ProposedPlanStep": "jaos.intelligence.models.proposed_plan_step",
    "ReasoningAssumption": "jaos.intelligence.models.reasoning_assumption",
    "ReasoningRequest": "jaos.intelligence.models.reasoning_request",
    "ReasoningResult": "jaos.intelligence.models.reasoning_result",
    "RiskLevel": "jaos.intelligence.models.risk_level",
}

__all__ = [
    "AgentAvailabilityState",
    "AgentDescriptor",
    "AgentHealthState",
    "AgentResult",
    "AgentTask",
    "AgentTaskStatus",
    "ContextBundle",
    "ContextItem",
    "ContextTrustLevel",
    "ConversationRole",
    "ConversationSession",
    "ConversationSessionState",
    "ConversationTurn",
    "ExecutionProposal",
    "FailureBehavior",
    "IntelligenceContextType",
    "IntelligenceIdentity",
    "IntelligenceRequest",
    "IntelligenceRequestType",
    "IntelligenceResult",
    "IntelligenceResultStatus",
    "IntelligenceScope",
    "PlanProposal",
    "PlanningConfiguration",
    "PlanningRequest",
    "ProposalStatus",
    "ProposedPlanStep",
    "ReasoningAssumption",
    "ReasoningRequest",
    "ReasoningResult",
    "RiskLevel",
]


def __getattr__(name: str) -> object:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(module_name), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
