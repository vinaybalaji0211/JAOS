
from logs.logger import logger


class ImprovementRecommendationEngine:

    @staticmethod
    def recommend(
            weaknesses,
            failures,
            low_scores):

        recommendations = []

        for weakness in weaknesses:
            recommendations.append(
                f"Improve weak area: {weakness}"
            )

        for failure in failures:
            recommendations.append(
                f"Fix repeated failure: {failure}"
            )

        for metric, score in low_scores.items():
            recommendations.append(
                f"Improve {metric}, current score is {score}"
            )

        if not recommendations:
            recommendations.append(
                "System performance is strong. Continue monitoring."
            )

        logger.info(
            "Improvement recommendations generated."
        )

        return recommendations

    @staticmethod
    def show_recommendations(
            weaknesses,
            failures,
            low_scores):

        recommendations = (
            ImprovementRecommendationEngine.recommend(
                weaknesses,
                failures,
                low_scores
            )
        )

        print("\nImprovement Recommendations:\n")

        for index, item in enumerate(
                recommendations,
                start=1):

            print(f"{index}. {item}")