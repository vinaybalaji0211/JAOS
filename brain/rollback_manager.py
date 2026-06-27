from logs.logger import logger


class RollbackManager:

    def __init__(self):

        self.rollback_history = []

    def create_checkpoint(
            self,
            version_name):

        self.rollback_history.append(
            {
                "version": version_name,
                "status": "CHECKPOINT"
            }
        )

        logger.info(
            f"Checkpoint created: "
            f"{version_name}"
        )

    def rollback(
            self,
            version_name):

        self.rollback_history.append(
            {
                "version": version_name,
                "status": "ROLLED_BACK"
            }
        )

        logger.info(
            f"Rollback executed: "
            f"{version_name}"
        )

    def show_history(self):

        print(
            "\nRollback Manager:\n"
        )

        if not self.rollback_history:

            print(
                "No rollback history."
            )

            return

        for item in self.rollback_history:

            print(
                f"Version: "
                f"{item['version']}"
            )

            print(
                f"Status: "
                f"{item['status']}"
            )

            print()