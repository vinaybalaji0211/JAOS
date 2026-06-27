from engineering.integration_test_runner import (
    IntegrationTestRunner
)

runner = IntegrationTestRunner()

runner.register_test(
    "Memory Platform"
)

runner.register_test(
    "Security Platform"
)

runner.register_test(
    "Dashboard Platform"
)

runner.run_tests()

runner.show_summary()