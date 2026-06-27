from logs.logger import logger


class MaintenanceScheduler:

    def __init__(self):
        self.maintenance_tasks = []

    def schedule(
            self,
            task_name,
            frequency,
            priority=1):

        task = {
            "task_name": task_name,
            "frequency": frequency,
            "priority": priority,
            "status": "SCHEDULED"
        }

        self.maintenance_tasks.append(task)

        self.maintenance_tasks.sort(
            key=lambda item: item["priority"]
        )

        logger.info(
            f"Maintenance scheduled: {task_name}"
        )

    def complete(
            self,
            task_name):

        for task in self.maintenance_tasks:
            if task["task_name"] == task_name:
                task["status"] = "COMPLETED"

                logger.info(
                    f"Maintenance completed: {task_name}"
                )

    def show_tasks(self):

        print("\nMaintenance Scheduler:\n")

        if not self.maintenance_tasks:
            print("No maintenance tasks.")
            return

        for index, task in enumerate(
                self.maintenance_tasks,
                start=1):

            print(
                f"{index}. "
                f"{task['task_name']} | "
                f"{task['frequency']} | "
                f"Priority {task['priority']} | "
                f"{task['status']}"
            )