from logs.logger import logger


class SelfEvaluationEngine:

    def __init__(self):

        self.metrics = {}

    def record_metric(
            self,
            metric_name,
            score):

        self.metrics[
            metric_name
        ] = score

        logger.info(
            f"Metric recorded: {metric_name}"
        )

    def evaluate(self):

        if not self.metrics:

            return "NO DATA"

        average = sum(
            self.metrics.values()
        ) / len(
            self.metrics
        )

        if average >= 90:
            return "EXCELLENT"

        elif average >= 75:
            return "GOOD"

        elif average >= 50:
            return "AVERAGE"

        return "NEEDS IMPROVEMENT"

    def show_evaluation(self):

        print("\nSelf Evaluation Engine:\n")

        for metric, score in self.metrics.items():

            print(
                f"{metric}: {score}"
            )

        print(
            f"\nOverall: {self.evaluate()}"
        )