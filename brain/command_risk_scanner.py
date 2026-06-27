from logs.logger import logger


class CommandRiskScanner:

    BLOCKED_KEYWORDS = [
        "format",
        "rm -rf",
        "del /s",
        "del /f",
        "rmdir /s",
        "shutdown",
        "taskkill /f"
    ]

    REVIEW_KEYWORDS = [
        "powershell",
        "cmd /c",
        "pip install",
        "npm install",
        "git clone",
        "taskkill",
        "reg add",
        "reg delete"
    ]

    @staticmethod
    def scan(command):

        command_lower = command.lower()

        for keyword in CommandRiskScanner.BLOCKED_KEYWORDS:

            if keyword in command_lower:

                decision = "BLOCKED"

                logger.warning(
                    f"Blocked risky command: {command}"
                )

                return decision

        for keyword in CommandRiskScanner.REVIEW_KEYWORDS:

            if keyword in command_lower:

                decision = "REVIEW_REQUIRED"

                logger.warning(
                    f"Command needs review: {command}"
                )

                return decision

        logger.info(
            f"Command scanned safe: {command}"
        )

        return "SAFE"

    @staticmethod
    def show_scan(command):

        decision = CommandRiskScanner.scan(
            command
        )

        print("\nCommand Risk Scanner:\n")

        print(
            f"Command: {command}"
        )

        print(
            f"Decision: {decision}"
        )