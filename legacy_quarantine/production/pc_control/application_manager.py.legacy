from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class ApplicationManager(BasePlatformService):
    """Runtime-managed PC application manager service."""

    SERVICE_NAME = "application_manager"

    def __init__(self, runtime=None):
        self.applications = {}

        super().__init__(runtime)

    def register_application(self, name, executable, status="AVAILABLE"):
        self.applications[name] = {
            "executable": executable,
            "status": status,
        }

        logger.info(f"Application registered: {name}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "application_registered",
                {
                    "name": name,
                    "executable": executable,
                    "status": status,
                },
            )

    def show_applications(self):
        print("\n=== Application Manager ===\n")

        if not self.applications:
            print("No applications registered.")
            return

        for app, data in self.applications.items():
            print(app)
            print(f"  Executable : {data['executable']}")
            print(f"  Status     : {data['status']}")
            print()