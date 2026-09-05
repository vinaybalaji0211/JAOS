from logs.logger import logger


class SystemHealthDashboard:

    def __init__(self):

        self.health = {}

    def update_status(
            self,
            component,
            status):

        self.health[component] = status

        logger.info(
            f"Health updated: {component}"
        )

    def show_health(self):

        print("\n=== System Health Dashboard ===\n")

        if not self.health:

            print("No health information.")
            return

        for component, status in self.health.items():

            print(component)
            print(f"  Status : {status}")
            print()