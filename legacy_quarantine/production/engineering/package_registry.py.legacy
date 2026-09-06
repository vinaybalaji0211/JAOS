from logs.logger import logger


class PackageRegistry:

    def __init__(self):
        self.packages = {}

    def register_package(
            self,
            name,
            version,
            status="INSTALLED"):

        self.packages[name] = {
            "version": version,
            "status": status
        }

        logger.info(
            f"Package registered: {name}"
        )

    def show_packages(self):

        print("\n========== PACKAGE REGISTRY ==========\n")

        if not self.packages:
            print("No registered packages.")
            return

        for name, data in self.packages.items():
            print(name)
            print(f"  Version : {data['version']}")
            print(f"  Status  : {data['status']}")
            print()