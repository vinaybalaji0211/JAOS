from brain.agent_registry import AgentRegistry


registry = AgentRegistry()

registry.register_agent(
    "Research Agent",
    "research",
    ["web_search", "fact_checking"]
)

registry.register_agent(
    "Coding Agent",
    "coding",
    ["write_code", "debug_code"]
)

registry.register_agent(
    "Security Agent",
    "security",
    ["threat_detection", "audit_logs"]
)

registry.update_status(
    "Research Agent",
    "BUSY"
)

registry.show_agents()