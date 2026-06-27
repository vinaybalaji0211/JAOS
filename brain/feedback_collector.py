from logs.logger import logger


class FeedbackCollector:

    def __init__(self):

        self.experiences = []

    def add_experience(
            self,
            task,
            result,
            reason,
            lesson,
            next_action,
            confidence,
            provider):

        experience = {

            "task": task,

            "result": result,

            "reason": reason,

            "lesson": lesson,

            "next_action": next_action,

            "confidence": confidence,

            "provider": provider

        }

        self.experiences.append(
            experience
        )

        logger.info(
            f"Experience added: {task}"
        )

    def show_experiences(self):

        print("\nExperience History:\n")

        if not self.experiences:

            print(
                "No experiences collected."
            )

            return

        for index, exp in enumerate(
                self.experiences,
                start=1):

            print(
                f"{index}. Task: {exp['task']}"
            )

            print(
                f"   Result: {exp['result']}"
            )

            print(
                f"   Reason: {exp['reason']}"
            )

            print(
                f"   Lesson: {exp['lesson']}"
            )

            print(
                f"   Next Action: {exp['next_action']}"
            )

            print(
                f"   Confidence: {exp['confidence']}"
            )

            print(
                f"   Provider: {exp['provider']}"
            )

            print()