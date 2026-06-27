from logs.logger import logger


class CloudBackupEngine:

    def __init__(self):

        self.backups = []

    def create_backup(
            self,
            backup_name):

        self.backups.append(
            {
                "backup": backup_name,
                "status": "CREATED"
            }
        )

        logger.info(
            f"Backup created: "
            f"{backup_name}"
        )

    def verify_backup(
            self,
            backup_name):

        for backup in self.backups:

            if backup["backup"] == backup_name:

                backup["status"] = (
                    "VERIFIED"
                )

    def show_backups(self):

        print(
            "\nCloud Backup Engine:\n"
        )

        if not self.backups:

            print(
                "No backups."
            )

            return

        for backup in self.backups:

            print(
                f"Backup: "
                f"{backup['backup']}"
            )

            print(
                f"Status: "
                f"{backup['status']}"
            )

            print()