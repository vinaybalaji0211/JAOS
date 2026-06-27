from logs.logger import logger


class PlatformRegistry:

    def __init__(self):
        self.platforms = {}

    def register_platform(
            self,
            name,
            version,
            status="ACTIVE",
            certified=False):

        self.platforms[name] = {
            "version": version,
            "status": status,
            "certified": certified
        }

        logger.info(
            f"Platform registered: {name}"
        )

    def show_platforms(self):

        print("\n========== PLATFORM REGISTRY ==========\n")

        if not self.platforms:
            print("No registered platforms.")
            return

        for name, data in self.platforms.items():

            print(name)
            print(f"  Version   : {data['version']}")
            print(f"  Status    : {data['status']}")
            print(f"  Certified : {data['certified']}")
            print()