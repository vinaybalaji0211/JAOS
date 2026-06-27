from logs.logger import logger


class KernelServiceRegistry:

    def __init__(self):
        self.services = {}

    def register_service(
            self,
            name,
            status="READY"):

        self.services[name] = status

        logger.info(
            f"Kernel service registered: {name}"
        )

    def show_services(self):

        print("\n========== KERNEL SERVICES ==========\n")

        if not self.services:
            print("No services registered.")
            return

        for name, status in self.services.items():
            print(f"{name}: {status}")