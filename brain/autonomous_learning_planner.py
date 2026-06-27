from logs.logger import logger


class AutonomousLearningPlanner:

    def __init__(self):

        self.learning_plans = {}

    def create_plan(
            self,
            subject,
            topics):

        self.learning_plans[
            subject
        ] = topics

        logger.info(
            f"Learning plan created: "
            f"{subject}"
        )

    def show_plan(
            self,
            subject):

        print(
            f"\nLearning Plan: "
            f"{subject}\n"
        )

        topics = self.learning_plans.get(
            subject,
            []
        )

        if not topics:

            print(
                "No plan found."
            )

            return

        for index, topic in enumerate(
                topics,
                start=1):

            print(
                f"{index}. {topic}"
            )