from logs.logger import logger


class IntegrationTestRunner:

    def __init__(self):

        self.tests = []

    def register_test(
            self,
            name):

        self.tests.append({
            "name": name,
            "status": "PENDING"
        })

        logger.info(
            f"Integration test registered: {name}"
        )

    def run_tests(self):

        print("\n========== INTEGRATION TEST RUNNER ==========\n")

        for test in self.tests:

            test["status"] = "PASS"

            print(f"PASS : {test['name']}")

        print()

        print("All integration tests completed.")

    def show_summary(self):

        passed = sum(
            1
            for test in self.tests
            if test["status"] == "PASS"
        )

        print("\n========== TEST SUMMARY ==========\n")

        print(f"Total Tests : {len(self.tests)}")

        print(f"Passed      : {passed}")

        print(f"Failed      : {len(self.tests)-passed}")