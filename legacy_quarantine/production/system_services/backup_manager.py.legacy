from logs.logger import logger


class BackupManager:

    def __init__(self):

        self.backups = []

    def register_backup(
            self,
            name,
            location,
            status="READY"):

        self.backups.append({
            "name": name,
            "location": location,
            "status": status
        })

        logger.info(
            f"Backup registered: {name}"
        )

    def show_backups(self):

        print("\n=== Backup Manager ===\n")

        if not self.backups:

            print("No backups.")
            return

        for backup in self.backups:

            print(backup["name"])
            print(f"  Location : {backup['location']}")
            print(f"  Status   : {backup['status']}")
            print()