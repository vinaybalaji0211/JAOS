from logs.logger import logger


class UpgradeRecommendationEngine:

    def __init__(self):

        self.recommendations = []

    def recommend_upgrade(
            self,
            weakness,
            recommendation,
            benefit):

        self.recommendations.append(
            {
                "weakness": weakness,
                "recommendation": recommendation,
                "benefit": benefit
            }
        )

        logger.info(
            f"Upgrade recommended: {recommendation}"
        )

    def show_recommendations(self):

        print(
            "\nUpgrade Recommendation Engine:\n"
        )

        if not self.recommendations:

            print(
                "No recommendations."
            )

            return

        for item in self.recommendations:

            print(
                f"Weakness: {item['weakness']}"
            )

            print(
                f"Recommendation: "
                f"{item['recommendation']}"
            )

            print(
                f"Benefit: "
                f"{item['benefit']}"
            )

            print()