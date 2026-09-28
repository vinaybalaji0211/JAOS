from logs.logger import logger


class TaskManager:

    def __init__(self):

        self.tasks = {}

    def create_task(
            self,
            task_name,
            priority="MEDIUM"):

        self.tasks[task_name] = {
            "priority": priority,
            "status": "CREATED"
        }

        logger.info(
            f"Task created: {task_name}"
        )

    def update_status(
            self,
            task_name,
            status):

        if task_name in self.tasks:

            self.tasks[
                task_name
            ]["status"] = status

    def show_tasks(self):

        print("\n=== Task Manager ===\n")

        if not self.tasks:

            print(
                "No tasks."
            )

            return

        for task, data in self.tasks.items():

            print(task)

            print(
                f"  Priority : {data['priority']}"
            )

            print(
                f"  Status   : {data['status']}"
            )

            print()