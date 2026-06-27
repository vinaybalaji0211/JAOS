from logs.logger import logger


class EvolutionMemory:

    def __init__(self):

        self.history = []

    def record_event(
            self,
            event_type,
            description):

        self.history.append(
            {
                "event_type": event_type,
                "description": description
            }
        )

        logger.info(
            f"Evolution event: {event_type}"
        )

    def show_history(self):

        print(
            "\nEvolution Memory:\n"
        )

        if not self.history:

            print(
                "No evolution history."
            )

            return

        for index, item in enumerate(
                self.history,
                start=1):

            print(
                f"{index}. "
                f"{item['event_type']}"
            )

            print(
                f"   {item['description']}"
            )

            print()