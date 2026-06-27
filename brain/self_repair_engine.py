from logs.logger import logger


class SelfRepairEngine:

    REPAIR_ACTIONS = {
        "missing_file": "Recreate the missing file.",
        "import_error": "Check module path and __init__.py files.",
        "config_error": "Validate or recreate config file.",
        "provider_failure": "Switch provider or check API/config.",
        "memory_corruption": "Restore memory from backup or reset corrupted file."
    }

    @staticmethod
    def diagnose(problem_type):

        action = SelfRepairEngine.REPAIR_ACTIONS.get(
            problem_type,
            "Manual inspection required."
        )

        logger.info(
            f"Repair diagnosis completed for: {problem_type}"
        )

        return action

    @staticmethod
    def show_repair(problem_type):

        action = SelfRepairEngine.diagnose(
            problem_type
        )

        print("\nSelf Repair Engine:\n")

        print(
            f"Problem: {problem_type}"
        )

        print(
            f"Repair Action: {action}"
        )