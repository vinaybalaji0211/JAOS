from logs.logger import logger


class ResponseStrategyManager:

    def __init__(self):

        self.current_strategy = "DETAILED"

    def set_strategy(
            self,
            strategy):

        self.current_strategy = strategy

        logger.info(
            f"Response strategy: {strategy}"
        )

    def get_strategy(self):

        return self.current_strategy

    def show_strategy(self):

        print(
            "\nResponse Strategy Manager:\n"
        )

        print(
            f"Current Strategy: "
            f"{self.current_strategy}"
        )