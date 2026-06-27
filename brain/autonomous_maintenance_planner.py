from logs.logger import logger


class AutonomousMaintenancePlanner:

    @staticmethod
    def plan(
            health_status,
            error_type=None,
            resource_problem=None,
            crash_detected=False,
            repair_needed=False):

        actions = []

        if health_status in ["WARNING", "CRITICAL"]:
            actions.append(
                "Run diagnostics"
            )

        if error_type:
            actions.append(
                f"Recover from error: {error_type}"
            )

        if resource_problem:
            actions.append(
                f"Recover resource problem: {resource_problem}"
            )

        if crash_detected:
            actions.append(
                "Restore last checkpoint"
            )

        if repair_needed:
            actions.append(
                "Run self repair"
            )

        if not actions:
            actions.append(
                "System healthy. No maintenance required."
            )

        logger.info(
            "Autonomous maintenance plan generated."
        )

        return actions

    @staticmethod
    def show_plan(
            health_status,
            error_type=None,
            resource_problem=None,
            crash_detected=False,
            repair_needed=False):

        actions = AutonomousMaintenancePlanner.plan(
            health_status,
            error_type,
            resource_problem,
            crash_detected,
            repair_needed
        )

        print("\nAutonomous Maintenance Plan:\n")

        for index, action in enumerate(
                actions,
                start=1):

            print(
                f"{index}. {action}"
            )