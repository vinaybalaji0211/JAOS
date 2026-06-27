from logs.logger import logger


class EventSystem:

    def __init__(self):

        self.events = []

    def emit(
            self,
            event_type,
            data=None):

        event = {
            "type": event_type,
            "data": data
        }

        self.events.append(event)

        logger.info(
            f"Event emitted: {event_type}"
        )

    def get_events(self):

        return self.events

    def show_events(self):

        print("\nEvent System:\n")

        if not self.events:

            print("No events.")

            return

        for index, event in enumerate(
                self.events,
                start=1):

            print(
                f"{index}. {event['type']} | {event['data']}"
            )