from brain.agent_security_firewall import AgentSecurityFirewall

firewall = AgentSecurityFirewall()

firewall.register_agent(
    "ResearchAgent",
    [
        "WEB_ACCESS",
        "READ_DOCUMENTS"
    ]
)

firewall.register_agent(
    "MemoryAgent",
    [
        "MEMORY_READ",
        "MEMORY_WRITE"
    ]
)

print(
    firewall.validate_access(
        "ResearchAgent",
        "WEB_ACCESS"
    )
)

print(
    firewall.validate_access(
        "ResearchAgent",
        "MEMORY_WRITE"
    )
)

firewall.show_agents()