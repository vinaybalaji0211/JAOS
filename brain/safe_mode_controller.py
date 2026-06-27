from logs.logger import logger


class SafeModeController:

    def __init__(self):

        self.safe_mode = False

        self.reason = None

    def activate(
            self,
            reason):

        self.safe_mode = True

        self.reason = reason

        logger.warning(
            f"SAFE MODE ACTIVATED: {reason}"
        )

    def deactivate(self):

        self.safe_mode = False

        self.reason = None

        logger.info(
            "Safe mode deactivated."
        )

    def show_status(self):

        print(
            "\nSafe Mode Controller:\n"
        )

        print(
            f"Safe Mode: "
            f"{self.safe_mode}"
        )

        print(
            f"Reason: "
            f"{self.reason}"
        )