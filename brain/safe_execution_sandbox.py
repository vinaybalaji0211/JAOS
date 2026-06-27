from logs.logger import logger


class SafeExecutionSandbox:

    SANDBOX_RULES = {

        "RUN_DIAGNOSTICS":
            "READ_ONLY",

        "READ_MEMORY":
            "READ_ONLY",

        "INSTALL_PACKAGE":
            "LIMITED",

        "EDIT_CONFIG":
            "LIMITED",

        "DELETE_FILE":
            "BLOCKED",

        "FORMAT_DISK":
            "BLOCKED"

    }

    @staticmethod
    def evaluate(
            action):

        level = (
            SafeExecutionSandbox
            .SANDBOX_RULES
            .get(

                action,

                "LIMITED"

            )
        )

        logger.info(
            f"Sandbox level: {action} -> {level}"
        )

        return level

    @staticmethod
    def show_level(
            action):

        level = (
            SafeExecutionSandbox
            .evaluate(
                action
            )
        )

        print("\nSafe Execution Sandbox:\n")

        print(
            f"Action: {action}"
        )

        print(
            f"Sandbox Level: {level}"
        )