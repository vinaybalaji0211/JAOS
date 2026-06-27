import os

from logs.logger import logger


class TestRunner:

    @staticmethod
    def run_tests():

        print("\nRunning System Tests...\n")

        required_files = [

            "core/engine.py",
            "core/module_loader.py",
            "core/event_system.py",
            "core/error_handler.py",
            "core/health_monitor.py",
            "core/snapshot_manager.py",
            "core/recovery_manager.py",
            "core/action_history.py",
            "core/plugin_manager.py"

        ]

        passed = 0

        for file in required_files:

            if os.path.exists(file):

                print(f"[PASS] {file}")

                passed += 1

            else:

                print(f"[FAIL] {file}")

        logger.info(
            f"Tests completed. {passed}/{len(required_files)} passed."
        )

        print(
            f"\n{passed}/{len(required_files)} tests passed."
        )