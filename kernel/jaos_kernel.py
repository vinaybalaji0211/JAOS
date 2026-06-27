from logs.logger import logger


class JAOSKernel:

    def __init__(self):

        self.platforms = {}

        self.status = "INITIALIZED"

    def register_platform(
            self,
            name,
            platform_object=None,
            status="REGISTERED"):

        self.platforms[name] = {
            "object": platform_object,
            "status": status
        }

        logger.info(
            f"Kernel registered platform: {name}"
        )

    def start(self):

        self.status = "ONLINE"

        logger.info(
            "JAOS Kernel started."
        )

        print("\n========== JAOS KERNEL ==========\n")
        print("Kernel Status : ONLINE")
        print("Mode          : v1 Alpha Stabilization")
        print("\n=================================\n")

    def show_platforms(self):

        print("\n========== KERNEL PLATFORM REGISTRY ==========\n")

        if not self.platforms:

            print("No platforms registered.")
            return

        for name, data in self.platforms.items():

            print(name)
            print(f"  Status : {data['status']}")
            print()