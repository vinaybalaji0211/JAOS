from logs.logger import logger


class PlatformStatusDashboard:

    def __init__(self):

        self.platforms = {}

    def register_platform(
            self,
            name,
            status,
            certified):

        self.platforms[name] = {
            "status": status,
            "certified": certified
        }

        logger.info(
            f"Platform registered: {name}"
        )

    def show_platforms(self):

        print("\n=== Platform Status Dashboard ===\n")

        if not self.platforms:

            print("No platforms registered.")
            return

        for name, data in self.platforms.items():

            print(name)

            print(
                f"  Status      : {data['status']}"
            )

            print(
                f"  Certified   : {data['certified']}"
            )

            print()