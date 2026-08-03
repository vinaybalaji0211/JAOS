from brain.coding_agent import CodingAgent

agent = CodingAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Review this Python module"
    )
)

print(
    agent.handle_task(
        "Debug this error"
    )
)

print(
    agent.handle_task(
        "Create unit tests"
    )
)