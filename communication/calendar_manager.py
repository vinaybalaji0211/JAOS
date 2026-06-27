from logs.logger import logger


class CalendarManager:

    def __init__(self):

        self.events = []

    def add_event(
            self,
            title,
            schedule):

        self.events.append(
            {
                "title": title,
                "schedule": schedule
            }
        )

        logger.info(
            f"Calendar event added: {title}"
        )

    def show_events(self):

        print("\n=== Calendar Manager ===\n")

        if not self.events:

            print("No events.")
            return

        for event in self.events:

            print(
                event["title"]
            )

            print(
                f"  Schedule : {event['schedule']}"
            )

            print()