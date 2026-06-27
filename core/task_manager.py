from logs.logger import logger


class TaskManager:

    def __init__(self):

        self.tasks = []

    def add_task(self, task):

        self.tasks.append(task)

        logger.info(
            f"Task added: {task}"
        )

    def show_tasks(self):

        print("\nTasks:")

        if not self.tasks:

            print("No tasks.")

        else:

            for index, task in enumerate(
                    self.tasks,
                    start=1):

                print(
                    f"{index}. {task}"
                )

    def clear_tasks(self):

        self.tasks.clear()

        logger.info(
            "Tasks cleared."
        )