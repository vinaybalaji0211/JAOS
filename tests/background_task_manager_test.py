from brain.background_task_manager import BackgroundTaskManager

manager = BackgroundTaskManager()

manager.add_task(
    "Health Monitor"
)

manager.add_task(
    "Memory Consolidation"
)

manager.show_tasks()

manager.stop_task(
    "Health Monitor"
)

manager.show_tasks()