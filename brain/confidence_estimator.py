from logs.logger import logger


class ConfidenceEstimator:

    @staticmethod
    def estimate(
            provider_confidence,
            memory_confidence,
            reality_confidence,
            resource_confidence,
            goal_confidence,
            conflict_count):

        total = (
            provider_confidence
            + memory_confidence
            + reality_confidence
            + resource_confidence
            + goal_confidence
        )

        average = total / 5

        penalty = conflict_count * 10

        final_confidence = max(
            0,
            round(
                average - penalty,
                2
            )
        )

        logger.info(
            f"Confidence estimated: {final_confidence}"
        )

        return {

            "provider_confidence":
                provider_confidence,

            "memory_confidence":
                memory_confidence,

            "reality_confidence":
                reality_confidence,

            "resource_confidence":
                resource_confidence,

            "goal_confidence":
                goal_confidence,

            "conflict_penalty":
                penalty,

            "final_confidence":
                final_confidence

        }

    @staticmethod
    def show_confidence(
            provider_confidence,
            memory_confidence,
            reality_confidence,
            resource_confidence,
            goal_confidence,
            conflict_count):

        result = ConfidenceEstimator.estimate(

            provider_confidence,

            memory_confidence,

            reality_confidence,

            resource_confidence,

            goal_confidence,

            conflict_count

        )

        print("\nConfidence Report:\n")

        for key, value in result.items():

            print(
                f"{key}: {value}"
            )