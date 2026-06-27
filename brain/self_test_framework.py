from logs.logger import logger


class SelfTestFramework:

    def __init__(self):

        self.test_results = []

    def run_test(
            self,
            test_name,
            result):

        self.test_results.append(
            {
                "test": test_name,
                "result": result
            }
        )

        logger.info(
            f"Test executed: {test_name}"
        )

    def show_results(self):

        print(
            "\nSelf-Test Framework:\n"
        )

        if not self.test_results:

            print(
                "No tests executed."
            )

            return

        for item in self.test_results:

            print(
                f"Test: {item['test']}"
            )

            print(
                f"Result: {item['result']}"
            )

            print()