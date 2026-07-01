from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class StartupManager(BasePlatformService):
    """Runtime-managed startup service."""

    SERVICE_NAME = "startup_manager"

    def __init__(self, runtime=None):
        self.services = {}

        super().__init__(runtime)

    def register_service(
        self,
        name,
        enabled=True,
    ):
        self.services[name] = enabled

        logger.info(
            f"Startup service registered: {name}"
        )

        if self.runtime is not None:
            self.runtime.events.publish(
                "startup_service_registered",
                {
                    "service": name,
                    "enabled": enabled,
                },
            )

    def show_services(self):
        print("\n=== Startup Manager ===\n")

        if not self.services:
            print("No startup services.")
            return

        for service, enabled in self.services.items():
            print(service)
            print(f"  Enabled : {enabled}")
            print()