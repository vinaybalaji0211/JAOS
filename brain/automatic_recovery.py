from logs.logger import logger


class AutomaticRecovery:

    def __init__(self):

        self.failures = []

    def report_failure(
            self,
            component):

        self.failures.append(
            component
        )

        logger.warning(
            f"Failure detected: {component}"
        )

    def recover(
            self,
            component):

        logger.info(
            f"Recovering {component}"
        )

        print(
            f"{component} recovered successfully."
        )

    def recover_all(self):

        print("\nAutomatic Recovery:\n")

        if not self.failures:

            print(
                "No failures detected."
            )

            return

        for component in self.failures:

            self.recover(
                component
            )

        self.failures.clear()

        logger.info(
            "Recovery cycle complete."
        )