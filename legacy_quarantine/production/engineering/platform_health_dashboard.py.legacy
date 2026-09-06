from datetime import datetime

from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class PlatformHealthDashboard(BasePlatformService):
    """Runtime-managed engineering platform health service."""

    SERVICE_NAME = "platform_health_dashboard"

    def __init__(self, runtime=None):
        self.platforms = {}

        super().__init__(runtime)

    def update_platform(
        self,
        name,
        health,
        passed,
        failed,
        certified=False,
    ):
        self.platforms[name] = {
            "health": health,
            "passed": passed,
            "failed": failed,
            "certified": certified,
            "last_validation": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

        logger.info(f"Health updated: {name}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "platform_health_updated",
                {
                    "platform": name,
                    "health": health,
                    "passed": passed,
                    "failed": failed,
                    "certified": certified,
                },
            )

    def show_dashboard(self):
        print("\n========== PLATFORM HEALTH ==========\n")

        if not self.platforms:
            print("No platform health data.")
            return

        for name, data in self.platforms.items():
            print(name)
            print(f"  Health           : {data['health']}")
            print(f"  Tests Passed     : {data['passed']}")
            print(f"  Tests Failed     : {data['failed']}")
            print(f"  Certified        : {data['certified']}")
            print(f"  Last Validation  : {data['last_validation']}")
            print()