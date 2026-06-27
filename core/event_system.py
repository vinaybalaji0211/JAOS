from logs.logger import logger


class EventSystem:

    def __init__(self):

        self.events = []

    def emit(self, event_name):

        self.events.append(event_name)

        logger.info(f"Event emitted: {event_name}")

    def show_events(self):

        print("Events:")

        for event in self.events:

            print("-", event)