from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class CommunicationHub(BasePlatformService):
    """Runtime-managed communication hub service."""

    SERVICE_NAME = "communication_hub"

    def __init__(self, runtime=None):
        self.events = []

        super().__init__(runtime)

    def add_event(self, source, category, message):
        self.events.append(
            {
                "source": source,
                "category": category,
                "message": message,
            }
        )

        logger.info(f"Communication event: {source}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "communication_event_added",
                {
                    "source": source,
                    "category": category,
                    "message": message,
                },
            )

    def show_events(self):
        print("\n=== Communication Hub ===\n")

        if not self.events:
            print("No communication events.")
            return

        for event in self.events:
            print(f"[{event['source']}] {event['category']}")
            print(f"  {event['message']}")
            print()