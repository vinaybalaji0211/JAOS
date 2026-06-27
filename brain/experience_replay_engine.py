from logs.logger import logger


class ExperienceReplayEngine:

    @staticmethod
    def replay(experiences):

        insights = []

        for exp in experiences:

            result = exp.get("result")

            task = exp.get("task")

            lesson = exp.get("lesson")

            if result == "SUCCESS":

                insights.append(
                    f"Reuse strategy from {task}"
                )

            elif result == "FAILED":

                insights.append(
                    f"Avoid previous mistake in {task}: {lesson}"
                )

        logger.info(
            "Experience replay completed."
        )

        return insights

    @staticmethod
    def show_replay(experiences):

        insights = (
            ExperienceReplayEngine.replay(
                experiences
            )
        )

        print("\nExperience Replay:\n")

        if not insights:

            print(
                "No experiences to replay."
            )

            return

        for index, insight in enumerate(
                insights,
                start=1):

            print(
                f"{index}. {insight}"
            )