from core.task_manager import TaskManager

tm = TaskManager()

tm.add_task(
    "Initialize Memory System"
)

tm.add_task(
    "Load AI Provider"
)

tm.show_tasks()