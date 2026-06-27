from logs.logger import logger


class StorageIntelligence:

    def __init__(self):

        self.storage_options = {}

    def register_storage(
            self,
            name,
            storage_type,
            status):

        self.storage_options[name] = {
            "type": storage_type,
            "status": status
        }

        logger.info(
            f"Storage registered: {name}"
        )

    def get_storage(
            self,
            name):

        return self.storage_options.get(
            name
        )

    def show_storage(self):

        print("\n=== Storage Intelligence ===\n")

        if not self.storage_options:

            print("No storage registered.")
            return

        for name, data in self.storage_options.items():

            print(f"{name}")
            print(f"  Type   : {data['type']}")
            print(f"  Status : {data['status']}")
            print()