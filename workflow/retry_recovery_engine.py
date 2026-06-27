from logs.logger import logger


class RetryRecoveryEngine:

    def __init__(self):

        self.failures = []

    def register_failure(
            self,
            task,
            reason):

        self.failures.append(
            {
                "task": task,
                "reason": reason
            }
        )

        logger.warning(
            f"Failure detected: {task}"
        )

    def show_failures(self):

        print(
            "\n=== Retry & Recovery ===\n"
        )

        if not self.failures:

            print(
                "No failures."
            )

            return

        for item in self.failures:

            print(
                f"Task : {item['task']}"
            )

            print(
                f"Reason : {item['reason']}"
            )

            print()