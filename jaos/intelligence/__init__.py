"""Public facade for the JAOS AI Intelligence Platform.

Exports are resolved lazily so importing a completed Intelligence subplatform
does not also import paused reasoning, planning, agent, execution-proposal, or
Memory-context capability code. Existing public symbol exports and safe package
submodule attributes remain available through this facade on first access.
"""

from importlib import import_module

_CONTEXT_EXPORTS = frozenset(
    {
        "ContextBudgetManager",
        "ContextBudgetResult",
        "ContextConflictDetector",
        "ContextConflictResult",
        "ContextDeduplicationResult",
        "ContextDeduplicator",
        "ContextFilter",
        "ContextFilterResult",
        "ContextPolicy",
        "ContextPolicyRegistry",
        "ContextRanker",
        "ContextRankingResult",
        "ContextSourceRegistry",
        "ContextTokenEstimator",
        "ConversationHistoryContextSource",
        "DefaultIntelligenceContextManager",
        "MemoryContextSource",
        "StaticContextSource",
    }
)
_EXCEPTION_EXPORTS = frozenset(
    {
        "IntelligenceAgentError",
        "IntelligenceApprovalRequiredError",
        "IntelligenceComponentStateError",
        "IntelligenceContextError",
        "IntelligenceConversationError",
        "IntelligenceExecutionProposalError",
        "IntelligencePermissionError",
        "IntelligencePlanningError",
        "IntelligencePlatformError",
        "IntelligenceReasoningError",
        "IntelligenceRequestError",
        "IntelligenceValidationError",
    }
)
_INTERFACE_EXPORTS = frozenset(
    {
        "AgentOrchestrator",
        "ConversationEngine",
        "ExecutionProposalBuilder",
        "IntelligenceComponent",
        "IntelligenceContextManager",
        "IntelligenceContextSource",
        "IntelligenceEngine",
        "PlanningEngine",
        "PromptComposer",
        "ReasoningEngine",
    }
)
_MODEL_EXPORTS = frozenset(
    {
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
        "PlanningConfiguration",
        "PlanningRequest",
        "PlanProposal",
        "ProposalStatus",
        "ProposedPlanStep",
        "ReasoningAssumption",
        "ReasoningRequest",
        "ReasoningResult",
        "RiskLevel",
    }
)
_PROMPT_EXPORTS = frozenset(
    {
        "IntelligencePromptComposer",
        "IntelligencePromptTemplate",
        "MetadataSensitiveContextRedactor",
        "PromptCompositionRequest",
        "PromptCompositionResult",
        "PromptInjectionDetector",
        "PromptInjectionResult",
        "PromptOutputSchemaFormatter",
        "PromptOutputSchemaResult",
        "PromptProviderCapabilityResult",
        "PromptProviderCapabilityValidator",
        "PromptRedactionResult",
        "PromptRedactor",
        "PromptTemplateRegistry",
    }
)

_EXPORT_MODULES = {
    **{name: "jaos.intelligence.context" for name in _CONTEXT_EXPORTS},
    **{name: "jaos.intelligence.exceptions" for name in _EXCEPTION_EXPORTS},
    **{name: "jaos.intelligence.interfaces" for name in _INTERFACE_EXPORTS},
    **{name: "jaos.intelligence.models" for name in _MODEL_EXPORTS},
    **{name: "jaos.intelligence.prompt" for name in _PROMPT_EXPORTS},
}
_COMPATIBILITY_SUBMODULES = {
    "context": "jaos.intelligence.context",
    "exceptions": "jaos.intelligence.exceptions",
    "interfaces": "jaos.intelligence.interfaces",
    "models": "jaos.intelligence.models",
    "prompt": "jaos.intelligence.prompt",
}

__all__ = [
    "AgentAvailabilityState",
    "AgentDescriptor",
    "AgentHealthState",
    "AgentOrchestrator",
    "AgentResult",
    "AgentTask",
    "AgentTaskStatus",
    "ContextBudgetManager",
    "ContextBudgetResult",
    "ContextBundle",
    "ContextConflictDetector",
    "ContextConflictResult",
    "ContextDeduplicationResult",
    "ContextDeduplicator",
    "ContextFilter",
    "ContextFilterResult",
    "ContextItem",
    "ContextPolicy",
    "ContextPolicyRegistry",
    "ContextRanker",
    "ContextRankingResult",
    "ContextSourceRegistry",
    "ContextTokenEstimator",
    "ContextTrustLevel",
    "ConversationEngine",
    "ConversationHistoryContextSource",
    "ConversationRole",
    "ConversationSession",
    "ConversationSessionState",
    "ConversationTurn",
    "DefaultIntelligenceContextManager",
    "ExecutionProposal",
    "ExecutionProposalBuilder",
    "FailureBehavior",
    "IntelligenceAgentError",
    "IntelligenceApprovalRequiredError",
    "IntelligenceComponent",
    "IntelligenceComponentStateError",
    "IntelligenceContextError",
    "IntelligenceContextManager",
    "IntelligenceContextSource",
    "IntelligenceContextType",
    "IntelligenceConversationError",
    "IntelligenceEngine",
    "IntelligenceExecutionProposalError",
    "IntelligenceIdentity",
    "IntelligencePermissionError",
    "IntelligencePlanningError",
    "IntelligencePlatformError",
    "IntelligencePromptComposer",
    "IntelligencePromptTemplate",
    "IntelligenceReasoningError",
    "IntelligenceRequest",
    "IntelligenceRequestError",
    "IntelligenceRequestType",
    "IntelligenceResult",
    "IntelligenceResultStatus",
    "IntelligenceScope",
    "IntelligenceValidationError",
    "MemoryContextSource",
    "MetadataSensitiveContextRedactor",
    "PlanProposal",
    "PlanningConfiguration",
    "PlanningEngine",
    "PlanningRequest",
    "PromptComposer",
    "PromptCompositionRequest",
    "PromptCompositionResult",
    "PromptInjectionDetector",
    "PromptInjectionResult",
    "PromptOutputSchemaFormatter",
    "PromptOutputSchemaResult",
    "PromptProviderCapabilityResult",
    "PromptProviderCapabilityValidator",
    "PromptRedactionResult",
    "PromptRedactor",
    "PromptTemplateRegistry",
    "ProposalStatus",
    "ProposedPlanStep",
    "ReasoningAssumption",
    "ReasoningEngine",
    "ReasoningRequest",
    "ReasoningResult",
    "RiskLevel",
    "StaticContextSource",
]


def __getattr__(name: str) -> object:
    compatibility_module = _COMPATIBILITY_SUBMODULES.get(name)
    if compatibility_module is not None:
        value = import_module(compatibility_module)
        globals()[name] = value
        return value

    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(module_name), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(
        set(globals()) | set(__all__) | set(_COMPATIBILITY_SUBMODULES)
    )
