from logs.logger import logger


class ResourceRecoveryEngine:

    RECOVERY_ACTIONS = {

        "LOW_RAM":
            "Clear cache and reduce memory usage.",

        "HIGH_CPU":
            "Pause low-priority tasks.",

        "GPU_OOM":
            "Reduce batch size or use CPU fallback.",

        "DISK_FULL":
            "Delete temporary files and compress logs.",

        "NETWORK_ISSUE":
            "Retry connection or switch provider."

    }

    @staticmethod
    def recover(
            resource_problem):

        action = (

            ResourceRecoveryEngine
            .RECOVERY_ACTIONS
            .get(

                resource_problem,

                "Manual intervention required."

            )

        )

        logger.info(

            f"Resource recovery: {resource_problem}"

        )

        return action

    @staticmethod
    def show_recovery(
            resource_problem):

        action = (
            ResourceRecoveryEngine
            .recover(
                resource_problem
            )
        )

        print("\nResource Recovery:\n")

        print(
            f"Problem: {resource_problem}"
        )

        print(
            f"Recovery Action: {action}"
        )