from logs.logger import logger


class PriorityInterruptionManager:

    @staticmethod
    def evaluate(
            current_priority,
            interruption_priority):

        if interruption_priority >= 90:
            decision = "OVERRIDE"

        elif interruption_priority > current_priority:
            decision = "PAUSE_AND_HANDLE"

        elif interruption_priority >= 50:
            decision = "QUEUE"

        else:
            decision = "IGNORE"

        logger.info(
            f"Interruption decision: {decision}"
        )

        return decision

    @staticmethod
    def show_decision(
            current_priority,
            interruption_priority):

        decision = (
            PriorityInterruptionManager.evaluate(
                current_priority,
                interruption_priority
            )
        )

        print(
            "\nPriority Interruption Manager:\n"
        )

        print(
            f"Current Priority: "
            f"{current_priority}"
        )

        print(
            f"Interruption Priority: "
            f"{interruption_priority}"
        )

        print(
            f"Decision: "
            f"{decision}"
        )