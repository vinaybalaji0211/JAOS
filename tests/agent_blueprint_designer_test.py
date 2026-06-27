from brain.agent_blueprint_designer import (
    AgentBlueprintDesigner
)

designer = (
    AgentBlueprintDesigner()
)

designer.create_blueprint(
    "QuantumPhysicsAgent",
    "Quantum Physics Expert",
    [
        "Quantum Theory",
        "Wave Mechanics",
        "Quantum Computing"
    ],
    [
        "READ_KNOWLEDGE"
    ],
    [
        "KnowledgeGraph",
        "CloudMemory"
    ]
)

designer.show_blueprints()