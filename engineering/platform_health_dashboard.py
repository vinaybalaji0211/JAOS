from logs.logger import logger
from datetime import datetime


class PlatformHealthDashboard:

    def __init__(self):

        self.platforms = {}

    def update_platform(
            self,
            name,
            health,
            passed,
            failed,
            certified=False):

        self.platforms[name] = {

            "health": health,

            "passed": passed,

            "failed": failed,

            "certified": certified,

            "last_validation": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

        logger.info(
            f"Health updated: {name}"
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