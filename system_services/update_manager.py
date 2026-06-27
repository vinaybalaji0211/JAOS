from logs.logger import logger


class UpdateManager:

    def __init__(self):

        self.updates = []

    def register_update(
            self,
            name,
            version,
            status="AVAILABLE"):

        self.updates.append({
            "name": name,
            "version": version,
            "status": status
        })

        logger.info(
            f"Update registered: {name}"
        )

    def show_updates(self):

        print("\n=== Update Manager ===\n")

        if not self.updates:

            print("No updates.")
            return

        for update in self.updates:

            print(update["name"])
            print(f"  Version : {update['version']}")
            print(f"  Status  : {update['status']}")
            print()