from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class MissionControl(BasePlatformService):
    """Runtime-managed JAOS mission control dashboard service."""

    SERVICE_NAME = "mission_control"

    def __init__(self, runtime=None):
        self.version = "JAOS v1 Alpha"
        self.status = "ONLINE"
        self.platforms = 15
        self.user = "Vinay"

        super().__init__(runtime)

    def show_dashboard(self):
        print("\n========== JAOS MISSION CONTROL ==========\n")
        print(f"Version   : {self.version}")
        print(f"Status    : {self.status}")
        print(f"Platforms : {self.platforms}")
        print(f"User      : {self.user}")
        print("\n==========================================\n")

        logger.info("Mission Control displayed.")

        if self.runtime is not None:
            self.runtime.events.publish(
                "mission_control_displayed",
                {"status": self.status},
            )