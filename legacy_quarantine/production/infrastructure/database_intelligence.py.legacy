from logs.logger import logger


class DatabaseIntelligence:

    def __init__(self):

        self.databases = {}

    def register_database(
            self,
            name,
            database_type,
            status):

        self.databases[name] = {
            "type": database_type,
            "status": status
        }

        logger.info(
            f"Database registered: {name}"
        )

    def get_database(
            self,
            name):

        return self.databases.get(
            name
        )

    def show_databases(self):

        print("\n=== Database Intelligence ===\n")

        if not self.databases:

            print("No databases registered.")
            return

        for name, data in self.databases.items():

            print(f"{name}")
            print(f"  Type   : {data['type']}")
            print(f"  Status : {data['status']}")
            print()