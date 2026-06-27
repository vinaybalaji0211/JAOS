from brain.email_agent import EmailAgent

agent = EmailAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Read inbox emails"
    )
)

print(
    agent.handle_task(
        "Draft project update email"
    )
)

print(
    agent.handle_task(
        "Create email summary"
    )
)