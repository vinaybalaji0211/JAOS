from logs.logger import logger


class Scheduler:

    def __init__(self):

        self.tasks = {}

    def register_task(
            self,
            task_name,
            schedule):

        self.tasks[task_name] = schedule

        logger.info(
            f"Task scheduled: {task_name}"
        )

    def show_tasks(self):

        print("\n=== Scheduler ===\n")

        if not self.tasks:

            print("No scheduled tasks.")
            return

        for task, schedule in self.tasks.items():

            print(task)
            print(f"  Schedule : {schedule}")
            print()