from logs.logger import logger


class DecisionAnalysisEngine:

    def __init__(self):

        self.decisions = []

    def analyze(
            self,
            problem,
            options,
            recommendation):

        decision = {
            "problem": problem,
            "options": options,
            "recommendation": recommendation
        }

        self.decisions.append(
            decision
        )

        logger.info(
            f"Decision analyzed: "
            f"{problem}"
        )

    def show_decisions(self):

        print(
            "\nDecision Analysis Engine:\n"
        )

        if not self.decisions:

            print(
                "No decisions."
            )

            return

        for decision in self.decisions:

            print(
                f"Problem: "
                f"{decision['problem']}"
            )

            print(
                "Options:"
            )

            for option in (
                    decision["options"]):

                print(
                    f" - {option}"
                )

            print(
                f"Recommendation: "
                f"{decision['recommendation']}"
            )

            print()