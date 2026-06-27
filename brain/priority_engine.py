from logs.logger import logger


class PriorityEngine:

    def __init__(self):
        self.tasks = []

    def add_task(self, task_name, priority):
        task = {
            "task": task_name,
            "priority": priority
        }

        self.tasks.append(task)

        priority_order = {
            "CRITICAL": 0,
            "HIGH": 1,
            "NORMAL": 2,
            "LOW": 3
        }

        self.tasks.sort(
            key=lambda item: priority_order.get(
                item["priority"],
                99
            )
        )

        logger.info(f"Task prioritized: {task_name}")

    def show_tasks(self):
        print("\nPriority Engine:\n")

        if not self.tasks:
            print("No tasks.")
            return

        for index, task in enumerate(self.tasks, start=1):
            print(f"{index}. {task['task']} | {task['priority']}")