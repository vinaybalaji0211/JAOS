from logs.logger import logger


class PredictionEngine:

    @staticmethod
    def predict(
            resources_ok,
            capability_available,
            risk_level,
            conflict_count,
            confidence):

        predictions = []

        if not resources_ok:

            predictions.append(
                "Execution may fail due to insufficient resources."
            )

        if not capability_available:

            predictions.append(
                "Task may not complete because required capability is missing."
            )

        if risk_level == "HIGH":

            predictions.append(
                "Safety restriction is likely because risk is high."
            )

        if conflict_count > 0:

            predictions.append(
                "Confidence may decrease because knowledge conflicts exist."
            )

        if confidence < 60:

            predictions.append(
                "Execution result may be unreliable due to low confidence."
            )

        if not predictions:

            predictions.append(
                "Execution is likely to proceed successfully."
            )

        logger.info(
            "Prediction completed."
        )

        return predictions

    @staticmethod
    def show_predictions(
            resources_ok,
            capability_available,
            risk_level,
            conflict_count,
            confidence):

        predictions = PredictionEngine.predict(
            resources_ok,
            capability_available,
            risk_level,
            conflict_count,
            confidence
        )

        print("\nPrediction Report:\n")

        for index, prediction in enumerate(
                predictions,
                start=1):

            print(
                f"{index}. {prediction}"
            )