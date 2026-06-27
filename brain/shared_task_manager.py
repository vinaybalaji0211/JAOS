from logs.logger import logger


class SharedTaskManager:

    def __init__(self):

        self.tasks = []

    def create_task(
            self,
            task_name,
            assigned_agents):

        task = {
            "task": task_name,
            "agents": assigned_agents,
            "status": "PENDING"
        }

        self.tasks.append(task)

        logger.info(
            f"Task created: {task_name}"
        )

    def update_status(
            self,
            task_name,
            status):

        for task in self.tasks:

            if task["task"] == task_name:

                task["status"] = status

    def show_tasks(self):

        print(
            "\nShared Task Manager:\n"
        )

        if not self.tasks:

            print(
                "No tasks."
            )

            return

        for task in self.tasks:

            print(
                f"Task: {task['task']}"
            )

            print(
                f"Agents: {task['agents']}"
            )

            print(
                f"Status: {task['status']}"
            )

            print()