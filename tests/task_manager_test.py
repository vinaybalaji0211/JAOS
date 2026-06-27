from workflow.task_manager import (
    TaskManager
)

manager = TaskManager()

manager.create_task(
    "Build Portfolio",
    "HIGH"
)

manager.create_task(
    "Summarize Emails",
    "LOW"
)

manager.update_status(
    "Build Portfolio",
    "RUNNING"
)

manager.show_tasks()