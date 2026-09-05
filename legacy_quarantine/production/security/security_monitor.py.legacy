from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class SecurityMonitor(BasePlatformService):
    """Runtime-managed security monitoring service."""

    SERVICE_NAME = "security_monitor"

    def __init__(self, runtime=None):
        self.events = []

        super().__init__(runtime)

    def record_event(self, level, description):
        self.events.append({
            "level": level,
            "description": description,
        })

        logger.info(f"Security event: {level}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "security_event_recorded",
                {
                    "level": level,
                    "description": description,
                },
            )

    def show_events(self):
        print("\n=== Security Monitor ===\n")

        if not self.events:
            print("No security events.")
            return

        for event in self.events:
            print(f"[{event['level']}] {event['description']}")