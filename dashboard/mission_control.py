from logs.logger import logger


class MissionControl:

    def __init__(self):

        self.version = "JAOS v1 Alpha"

        self.status = "ONLINE"

        self.platforms = 15

        self.user = "Vinay"

    def show_dashboard(self):

        print("\n========== JAOS MISSION CONTROL ==========\n")

        print(f"Version   : {self.version}")

        print(f"Status    : {self.status}")

        print(f"Platforms : {self.platforms}")

        print(f"User      : {self.user}")

        print("\n==========================================\n")

        logger.info(
            "Mission Control displayed."
        )