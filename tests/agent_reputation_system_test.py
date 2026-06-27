from brain.agent_reputation_system import (
    AgentReputationSystem
)

system = (
    AgentReputationSystem()
)

system.register_agent(
    "ResearchAgent",
    90
)

system.register_agent(
    "MemoryAgent",
    95
)

system.register_agent(
    "NewQuantumAgent",
    50
)

system.increase_score(
    "ResearchAgent",
    5
)

system.decrease_score(
    "NewQuantumAgent",
    20
)

system.show_reputation()