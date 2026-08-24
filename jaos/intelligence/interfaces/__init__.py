"""Public interfaces for the JAOS AI Intelligence Platform.

The facade is lazy so a conversation-only runtime does not import interfaces
for paused planning, reasoning, agent, or execution-proposal capabilities.
"""

from importlib import import_module

_EXPORT_MODULES = {
    "AgentOrchestrator": "jaos.intelligence.interfaces.agent_orchestrator",
    "ConversationEngine": "jaos.intelligence.interfaces.conversation_engine",
    "ExecutionProposalBuilder": (
        "jaos.intelligence.interfaces.execution_proposal_builder"
    ),
    "IntelligenceComponent": (
        "jaos.intelligence.interfaces.intelligence_component"
    ),
    "IntelligenceContextManager": (
        "jaos.intelligence.interfaces.context_manager"
    ),
    "IntelligenceContextSource": "jaos.intelligence.interfaces.context_source",
    "IntelligenceEngine": "jaos.intelligence.interfaces.intelligence_engine",
    "PlanningEngine": "jaos.intelligence.interfaces.planning_engine",
    "PromptComposer": "jaos.intelligence.interfaces.prompt_composer",
    "ReasoningEngine": "jaos.intelligence.interfaces.reasoning_engine",
}

__all__ = [
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
