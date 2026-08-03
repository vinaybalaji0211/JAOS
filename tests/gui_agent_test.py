from brain.gui_agent import GUIAgent

agent = GUIAgent()

agent.show_capabilities()

print()

print(
    agent.execute(
        "click",
        "OK button"
    )
)

print(
    agent.execute(
        "type",
        "username field"
    )
)

print(
    agent.execute(
        "open",
        "VS Code"
    )
)