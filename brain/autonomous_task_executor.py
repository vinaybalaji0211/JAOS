from logs.logger import logger


class AutonomousTaskExecutor:

    def __init__(self):

        self.execution_history = []

    def execute_task(
            self,
            task_name):

        logger.info(
            f"Executing: {task_name}"
        )

        result = {
            "task": task_name,
            "status": "COMPLETED"
        }

        self.execution_history.append(
            result
        )

        return result

    def show_history(self):

        print(
            "\nExecution History:\n"
        )

        if not self.execution_history:

            print(
                "No tasks executed."
            )

            return

        for item in self.execution_history:

            print(
                f"{item['task']} "
                f"-> "
                f"{item['status']}"
            )