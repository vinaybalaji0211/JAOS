from brain.calendar_agent import CalendarAgent

agent = CalendarAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Create project review event"
    )
)

print(
    agent.handle_task(
        "Track exam deadline"
    )
)

print(
    agent.handle_task(
        "Optimize weekly schedule"
    )
)