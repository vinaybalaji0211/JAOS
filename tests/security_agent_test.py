from brain.security_agent import SecurityAgent

agent = SecurityAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Detect threat"
    )
)

print(
    agent.handle_task(
        "Run security audit"
    )
)

print(
    agent.handle_task(
        "Perform risk assessment"
    )
)