from logs.logger import logger


class RoadmapRecommendationEngine:

    def __init__(self):

        self.recommendations = []

    def recommend(
            self,
            feature,
            current_version,
            suggested_version,
            reason):

        recommendation = {
            "feature": feature,
            "current_version": current_version,
            "suggested_version": suggested_version,
            "reason": reason
        }

        self.recommendations.append(
            recommendation
        )

        logger.info(
            f"Roadmap recommendation: {feature}"
        )

    def show_recommendations(self):

        print(
            "\nRoadmap Recommendations\n"
        )

        if not self.recommendations:

            print(
                "No recommendations."
            )

            return

        for item in self.recommendations:

            print(
                f"Feature: {item['feature']}"
            )

            print(
                f"Current Version: {item['current_version']}"
            )

            print(
                f"Suggested Version: {item['suggested_version']}"
            )

            print(
                f"Reason: {item['reason']}"
            )

            print()