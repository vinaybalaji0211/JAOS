from logs.logger import logger


class BackgroundTaskManager:

    def __init__(self):

        self.tasks = []

    def add_task(
            self,
            task_name):

        task = {

            "name": task_name,

            "status": "RUNNING"

        }

        self.tasks.append(
            task
        )

        logger.info(
            f"Background task started: {task_name}"
        )

    def stop_task(
            self,
            task_name):

        for task in self.tasks:

            if task["name"] == task_name:

                task["status"] = "STOPPED"

                logger.info(
                    f"Background task stopped: {task_name}"
                )

    def show_tasks(self):

        print("\nBackground Tasks:\n")

        if not self.tasks:

            print(
                "No background tasks."
            )

            return

        for index, task in enumerate(
                self.tasks,
                start=1):

            print(

                f"{index}. "

                f"{task['name']} | "

                f"{task['status']}"

            )