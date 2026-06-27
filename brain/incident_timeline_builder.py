from logs.logger import logger


class IncidentTimelineBuilder:

    def __init__(self):

        self.timeline = []

    def add_event(
            self,
            timestamp,
            event):

        self.timeline.append(
            {
                "timestamp": timestamp,
                "event": event
            }
        )

        logger.info(
            f"Timeline event added: {event}"
        )

    def show_timeline(self):

        print(
            "\nIncident Timeline:\n"
        )

        if not self.timeline:

            print(
                "No events recorded."
            )

            return

        for item in sorted(
                self.timeline,
                key=lambda x: x["timestamp"]):

            print(
                f"{item['timestamp']} "
                f"-> "
                f"{item['event']}"
            )