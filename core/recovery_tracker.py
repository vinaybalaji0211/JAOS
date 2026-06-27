from logs.logger import logger


class RecoveryTracker:

    def __init__(self):

        self.recovery_events = []

    def record_event(self, event):

        self.recovery_events.append(event)

        logger.info(
            f"Recovery event recorded: {event}"
        )

    def show_events(self):

        print("\nRecovery Events:")

        if not self.recovery_events:

            print("No recovery events.")

        else:

            for index, event in enumerate(
                    self.recovery_events,
                    start=1):

                print(
                    f"{index}. {event}"
                )

    def clear_events(self):

        self.recovery_events.clear()

        logger.info(
            "Recovery events cleared."
        )