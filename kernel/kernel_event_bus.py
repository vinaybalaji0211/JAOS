from logs.logger import logger


class KernelEventBus:

    def __init__(self):
        self.events = []

    def publish_event(
            self,
            source,
            event_type,
            message):

        event = {
            "source": source,
            "type": event_type,
            "message": message
        }

        self.events.append(event)

        logger.info(
            f"Kernel event published: {event_type}"
        )

    def show_events(self):

        print("\n========== KERNEL EVENT BUS ==========\n")

        if not self.events:
            print("No events.")
            return

        for event in self.events:
            print(f"[{event['source']}] {event['type']}")
            print(f"  {event['message']}")
            print()