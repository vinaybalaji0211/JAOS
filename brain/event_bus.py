from logs.logger import logger


class EventBus:

    def __init__(self):

        self.subscribers = {}

        self.event_history = []

    def subscribe(self, event_name, callback):

        if event_name not in self.subscribers:

            self.subscribers[event_name] = []

        self.subscribers[event_name].append(callback)

        logger.info(
            f"Subscriber added for event: {event_name}"
        )

    def publish(self, event_name, data=None):

        event = {
            "event": event_name,
            "data": data
        }

        self.event_history.append(event)

        logger.info(
            f"Event published: {event_name}"
        )

        if event_name in self.subscribers:

            for callback in self.subscribers[event_name]:

                callback(data)

    def show_history(self):

        print("\nEvent History:")

        if not self.event_history:

            print("No events published.")

        else:

            for index, event in enumerate(
                    self.event_history,
                    start=1):

                print(
                    f"{index}. {event['event']} -> {event['data']}"
                )
                