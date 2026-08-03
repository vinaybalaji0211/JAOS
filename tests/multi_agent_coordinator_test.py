from brain.multi_agent_coordinator import MultiAgentCoordinator

coordinator = (
    MultiAgentCoordinator()
)

coordinator.create_project(
    "Quantum Research Analysis",
    [
        "ResearchAgent",
        "DocumentAgent",
        "MemoryAgent"
    ]
)

coordinator.complete_project(
    "Quantum Research Analysis"
)

coordinator.show_projects()