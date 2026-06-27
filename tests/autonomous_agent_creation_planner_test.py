from brain.autonomous_agent_creation_planner import (
    AutonomousAgentCreationPlanner
)

planner = (
    AutonomousAgentCreationPlanner()
)

planner.create_proposal(
    "QuantumPhysicsAgent",
    "Advanced quantum research"
)

planner.create_proposal(
    "MedicalResearchAgent",
    "Medical literature analysis"
)

planner.approve_proposal(
    "QuantumPhysicsAgent"
)

planner.show_proposals()