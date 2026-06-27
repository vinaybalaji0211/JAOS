from logs.logger import logger


class CommunicationHub:

    def __init__(self):

        self.events = []

    def add_event(
            self,
            source,
            category,
            message):

        self.events.append(
            {
                "source": source,
                "category": category,
                "message": message
            }
        )

        logger.info(
            f"Communication event: {source}"
        )

    def show_events(self):

        print(
            "\n=== Communication Hub ===\n"
        )

        if not self.events:

            print(
                "No communication events."
            )

            return

        for event in self.events:

            print(
                f"[{event['source']}] "
                f"{event['category']}"
            )

            print(
                f"  {event['message']}"
            )

            print()