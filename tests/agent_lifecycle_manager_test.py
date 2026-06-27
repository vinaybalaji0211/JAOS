from brain.agent_lifecycle_manager import (
    AgentLifecycleManager
)

manager = (
    AgentLifecycleManager()
)

manager.create_agent(
    "QuantumPhysicsAgent"
)

manager.update_status(
    "QuantumPhysicsAgent",
    "TRAINING"
)

manager.update_status(
    "QuantumPhysicsAgent",
    "ACTIVE"
)

manager.show_agents()

print(
    manager.get_status(
        "QuantumPhysicsAgent"
    )
)