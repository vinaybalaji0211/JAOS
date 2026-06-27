from logs.logger import logger


class SelfImprovementAnalyzer:

    def __init__(self):

        self.weaknesses = []

    def add_weakness(
            self,
            weakness,
            priority="MEDIUM"):

        self.weaknesses.append(
            {
                "weakness": weakness,
                "priority": priority
            }
        )

        logger.info(
            f"Weakness detected: {weakness}"
        )

    def show_analysis(self):

        print(
            "\nSelf Improvement Analyzer:\n"
        )

        if not self.weaknesses:

            print(
                "No weaknesses detected."
            )

            return

        for item in self.weaknesses:

            print(
                f"Weakness: "
                f"{item['weakness']}"
            )

            print(
                f"Priority: "
                f"{item['priority']}"
            )

            print()