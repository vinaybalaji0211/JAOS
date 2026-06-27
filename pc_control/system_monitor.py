from logs.logger import logger


class SystemMonitor:

    def __init__(self):

        self.metrics = {}

    def update_metric(
            self,
            metric,
            value):

        self.metrics[metric] = value

        logger.info(
            f"Metric updated: {metric}"
        )

    def show_metrics(self):

        print(
            "\n=== System Monitor ===\n"
        )

        if not self.metrics:

            print(
                "No metrics available."
            )

            return

        for metric, value in self.metrics.items():

            print(
                f"{metric}: {value}"
            )