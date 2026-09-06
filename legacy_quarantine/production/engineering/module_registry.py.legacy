from logs.logger import logger


class ModuleRegistry:

    def __init__(self):

        self.modules = {}

    def register_module(
            self,
            name,
            platform,
            version,
            status="ACTIVE",
            description=""):

        self.modules[name] = {

            "platform": platform,

            "version": version,

            "status": status,

            "description": description

        }

        logger.info(
            f"Module registered: {name}"
        )

    def show_modules(self):

        print("\n========== MODULE REGISTRY ==========\n")

        if not self.modules:

            print("No registered modules.")
            return

        for name, data in self.modules.items():

            print(name)

            print(f"  Platform   : {data['platform']}")

            print(f"  Version    : {data['version']}")

            print(f"  Status     : {data['status']}")

            print(f"  Description: {data['description']}")

            print()