from brain.agent_coordinator import AgentCoordinator


coordinator = AgentCoordinator()

coordinator.assign_task(
    "Coding Agent",
    "Review Python module"
)

coordinator.assign_task(
    "Security Agent",
    "Check command risk"
)

coordinator.show_tasks()

coordinator.update_result(
    "Coding Agent",
    "Code review completed"
)

coordinator.update_result(
    "Security Agent",
    "No dangerous command found"
)

coordinator.show_tasks()