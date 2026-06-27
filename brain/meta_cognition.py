from logs.logger import logger


class MetaCognition:

    @staticmethod
    def analyze(
            strengths,
            weaknesses,
            strategy_change,
            provider_preference,
            self_improvement_goal):

        report = {

            "strengths": strengths,

            "weaknesses": weaknesses,

            "strategy_change": strategy_change,

            "provider_preference":
                provider_preference,

            "self_improvement_goal":
                self_improvement_goal

        }

        logger.info(
            "Meta-cognition analysis completed."
        )

        return report

    @staticmethod
    def show_report(
            strengths,
            weaknesses,
            strategy_change,
            provider_preference,
            self_improvement_goal):

        report = MetaCognition.analyze(

            strengths,

            weaknesses,

            strategy_change,

            provider_preference,

            self_improvement_goal

        )

        print("\nMeta-Cognition Report:\n")

        print("Strengths:")

        for item in report["strengths"]:

            print(f"- {item}")

        print("\nWeaknesses:")

        for item in report["weaknesses"]:

            print(f"- {item}")

        print(
            f"\nStrategy Change: "
            f"{report['strategy_change']}"
        )

        print(
            f"Provider Preference: "
            f"{report['provider_preference']}"
        )

        print(
            f"Self Improvement Goal: "
            f"{report['self_improvement_goal']}"
        )