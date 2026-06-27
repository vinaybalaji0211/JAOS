from datetime import datetime
from logs.logger import logger


class KernelHealthMonitor:

    def __init__(self):

        self.components = {}

    def update_status(
            self,
            component,
            status):

        self.components[component] = {
            "status": status,
            "last_updated": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        logger.info(
            f"Kernel health updated: {component}"
        )

    def get_status(
            self,
            component):

        return self.components.get(component)

    def show_health(self):

        print("\n========== KERNEL HEALTH ==========\n")

        if not self.components:

            print("No health information.")
            return

        for component, data in self.components.items():

            print(component)
            print(f"  Status       : {data['status']}")
            print(f"  Last Updated : {data['last_updated']}")
            print()