from brain.pc_control_agent import (
    PCControlAgent
)

agent = PCControlAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Launch VS Code"
    )
)

print(
    agent.handle_task(
        "Monitor system resources"
    )
)

print(
    agent.handle_task(
        "Manage project files"
    )
)