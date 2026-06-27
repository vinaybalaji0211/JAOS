from logs.logger import logger


class CloudRecoveryManager:

    def __init__(self):

        self.recovery_history = []

    def recover(
            self,
            backup_name):

        record = {
            "backup": backup_name,
            "status": "RECOVERED"
        }

        self.recovery_history.append(
            record
        )

        logger.info(
            f"Recovery executed: "
            f"{backup_name}"
        )

    def show_recovery_history(self):

        print(
            "\nCloud Recovery Manager:\n"
        )

        if not self.recovery_history:

            print(
                "No recoveries executed."
            )

            return

        for record in self.recovery_history:

            print(
                f"Backup: "
                f"{record['backup']}"
            )

            print(
                f"Status: "
                f"{record['status']}"
            )

            print()