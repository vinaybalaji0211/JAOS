from brain.agent_conflict_resolver import AgentConflictResolver

resolver = (
    AgentConflictResolver()
)

resolver.report_conflict(
    "ResearchAgent",
    "SecurityAgent",
    "External API Usage"
)

resolver.report_conflict(
    "MemoryAgent",
    "CodingAgent",
    "Memory Update Method"
)

resolver.resolve_conflict(
    "External API Usage"
)

resolver.show_conflicts()