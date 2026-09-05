from logs.logger import logger


class CleanupManager:

    def __init__(self):

        self.tasks = []

    def register_cleanup(
            self,
            task):

        if task not in self.tasks:
            self.tasks.append(task)

            logger.info(
                f"Cleanup task registered: {task}"
            )

    def run_cleanup(self):

        print("\n=== Cleanup Manager ===\n")

        if not self.tasks:

            print("No cleanup tasks.")
            return

        for task in self.tasks:

            print(f"Cleaning: {task}")

        print("\nCleanup completed.")

    def show_tasks(self):

        print("\n=== Cleanup Tasks ===\n")

        if not self.tasks:

            print("No cleanup tasks.")
            return

        for task in self.tasks:

            print(task)