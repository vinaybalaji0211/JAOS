from logs.logger import logger


class ExperienceSummarizer:

    @staticmethod
    def summarize(experiences):
        total = len(experiences)

        successes = sum(
            1 for item in experiences
            if item.get("result") == "SUCCESS"
        )

        failures = sum(
            1 for item in experiences
            if item.get("result") == "FAILURE"
        )

        lessons = [
            item.get("lesson")
            for item in experiences
            if item.get("lesson")
        ]

        summary = {
            "total_experiences": total,
            "successes": successes,
            "failures": failures,
            "lessons": lessons
        }

        logger.info("Experience summary generated.")

        return summary

    @staticmethod
    def show_summary(experiences):
        summary = ExperienceSummarizer.summarize(
            experiences
        )

        print("\nExperience Summary:\n")
        print(f"Total: {summary['total_experiences']}")
        print(f"Successes: {summary['successes']}")
        print(f"Failures: {summary['failures']}")

        print("\nLessons:")
        for lesson in summary["lessons"]:
            print(f"- {lesson}")