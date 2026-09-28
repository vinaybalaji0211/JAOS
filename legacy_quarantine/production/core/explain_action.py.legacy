from logs.logger import logger


class ExplainAction:

    def __init__(self):

        self.explanations = []

    def record(self, action, reason):

        entry = {
            "action": action,
            "reason": reason
        }

        self.explanations.append(entry)

        logger.info(
            f"Explanation recorded: {action} -> {reason}"
        )

    def show_explanations(self):

        print("\nExplain My Action:")

        if not self.explanations:

            print("No explanations recorded.")

        else:

            for index, item in enumerate(
                    self.explanations,
                    start=1):

                print(
                    f"{index}. Action: {item['action']}"
                )

                print(
                    f"   Reason: {item['reason']}"
                )
                