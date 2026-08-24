"""Public context facade for the JAOS AI Intelligence Platform.

Exports are lazy so compatibility access to this package does not load the
deferred MemoryContextSource unless that capability is explicitly requested.
"""

from importlib import import_module

_EXPORT_MODULES = {
    "ContextBudgetManager": (
        "jaos.intelligence.context.context_budget_manager"
    ),
    "ContextBudgetResult": (
        "jaos.intelligence.context.context_budget_manager"
    ),
    "ContextConflictDetector": (
        "jaos.intelligence.context.context_conflict_detector"
    ),
    "ContextConflictResult": (
        "jaos.intelligence.context.context_conflict_detector"
    ),
    "ContextDeduplicationResult": (
        "jaos.intelligence.context.context_deduplicator"
    ),
    "ContextDeduplicator": (
        "jaos.intelligence.context.context_deduplicator"
    ),
    "ContextFilter": "jaos.intelligence.context.context_filter",
    "ContextFilterResult": "jaos.intelligence.context.context_filter",
    "ContextPolicy": "jaos.intelligence.context.context_policy",
    "ContextPolicyRegistry": (
        "jaos.intelligence.context.context_policy_registry"
    ),
    "ContextRanker": "jaos.intelligence.context.context_ranker",
    "ContextRankingResult": (
        "jaos.intelligence.context.context_ranker"
    ),
    "ContextSourceRegistry": (
        "jaos.intelligence.context.context_source_registry"
    ),
    "ContextTokenEstimator": (
        "jaos.intelligence.context.context_token_estimator"
    ),
    "ConversationHistoryContextSource": (
        "jaos.intelligence.context.conversation_history_context_source"
    ),
    "DefaultIntelligenceContextManager": (
        "jaos.intelligence.context.context_manager"
    ),
    "MemoryContextSource": (
        "jaos.intelligence.context.memory_context_source"
    ),
    "StaticContextSource": (
        "jaos.intelligence.context.static_context_source"
    ),
}

__all__ = [
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
