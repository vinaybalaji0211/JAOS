from brain.shared_task_manager import (
    SharedTaskManager
)

manager = (
    SharedTaskManager()
)

manager.create_task(
    "Analyze Quantum Paper",
    [
        "ResearchAgent",
        "DocumentAgent"
    ]
)

manager.update_status(
    "Analyze Quantum Paper",
    "IN_PROGRESS"
)

manager.show_tasks()