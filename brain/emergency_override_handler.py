from logs.logger import logger


class EmergencyOverrideHandler:

    def __init__(self):

        self.emergency_active = False
        self.last_emergency = None

    def trigger(
            self,
            emergency_type):

        self.emergency_active = True
        self.last_emergency = emergency_type

        logger.warning(
            f"Emergency override: {emergency_type}"
        )

    def clear(self):

        self.emergency_active = False

        logger.info(
            "Emergency cleared."
        )

    def show_status(self):

        print(
            "\nEmergency Override Handler:\n"
        )

        print(
            f"Emergency Active: "
            f"{self.emergency_active}"
        )

        print(
            f"Last Emergency: "
            f"{self.last_emergency}"
        )