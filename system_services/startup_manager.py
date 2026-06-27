from logs.logger import logger


class StartupManager:

    def __init__(self):

        self.services = {}

    def register_service(
            self,
            name,
            enabled=True):

        self.services[name] = enabled

        logger.info(
            f"Startup service registered: {name}"
        )

    def show_services(self):

        print("\n=== Startup Manager ===\n")

        if not self.services:

            print("No startup services.")
            return

        for service, enabled in self.services.items():

            print(service)
            print(f"  Enabled : {enabled}")
            print()