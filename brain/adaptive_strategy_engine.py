from logs.logger import logger


class AdaptiveStrategyEngine:

    def __init__(self):

        self.current_strategy = "BALANCED"

    def adapt(
            self,
            evaluation):

        if evaluation == "EXCELLENT":

            self.current_strategy = (
                "OPTIMIZATION"
            )

        elif evaluation == "GOOD":

            self.current_strategy = (
                "BALANCED"
            )

        elif evaluation == "AVERAGE":

            self.current_strategy = (
                "IMPROVEMENT"
            )

        else:

            self.current_strategy = (
                "RECOVERY"
            )

        logger.info(
            f"Adaptive strategy changed to "
            f"{self.current_strategy}"
        )

    def show_strategy(self):

        print(
            "\nAdaptive Strategy Engine:\n"
        )

        print(
            f"Current Strategy: "
            f"{self.current_strategy}"
        )