from logs.logger import logger


class Scheduler:

    def __init__(self):

        self.tasks = []

    def add_task(
            self,
            task_name,
            trigger_time):

        task = {

            "task_name": task_name,

            "trigger_time": trigger_time,

            "status": "PENDING"

        }

        self.tasks.append(
            task
        )

        logger.info(
            f"Task scheduled: {task_name}"
        )

    def complete_task(
            self,
            task_name):

        for task in self.tasks:

            if task["task_name"] == task_name:

                task["status"] = "COMPLETED"

                logger.info(
                    f"Task completed: {task_name}"
                )

    def show_tasks(self):

        print("\nScheduler:\n")

        if not self.tasks:

            print(
                "No scheduled tasks."
            )

            return

        for index, task in enumerate(
                self.tasks,
                start=1):

            print(

                f"{index}. "

                f"{task['task_name']} | "

                f"{task['trigger_time']} | "

                f"{task['status']}"

            )