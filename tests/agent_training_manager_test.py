from brain.agent_training_manager import (
    AgentTrainingManager
)

manager = (
    AgentTrainingManager()
)

manager.start_training(
    "QuantumPhysicsAgent",
    [
        "Classical Physics",
        "Wave Mechanics",
        "Quantum States"
    ]
)

manager.update_progress(
    "QuantumPhysicsAgent",
    75
)

manager.show_training()