from logs.logger import logger


class ErrorRecoveryEngine:

    def __init__(self):

        self.recovery_actions = {

            "PROVIDER_ERROR":
                "Switch provider",

            "GPU_OOM":
                "Reduce resource usage",

            "VOICE_FAILURE":
                "Restart voice system",

            "MEMORY_ERROR":
                "Clear memory cache"

        }

    def recover(
            self,
            error_type):

        action = self.recovery_actions.get(

            error_type,

            "Manual intervention required"

        )

        logger.info(

            f"Recovery action for {error_type}: {action}"

        )

        return action

    def show_recovery(
            self,
            error_type):

        action = self.recover(

            error_type

        )

        print("\nError Recovery:\n")

        print(

            f"Error: {error_type}"

        )

        print(

            f"Recovery Action: {action}"

        )