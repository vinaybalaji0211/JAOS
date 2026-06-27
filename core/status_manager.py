from logs.logger import logger


class StatusManager:

    def __init__(self):

        self.status = {

            "name": "JARVIS OS",

            "state": "ONLINE",

            "phase": "Phase 1",

            "mode": "NORMAL"

        }

    def get_status(self):

        logger.info("Status requested.")

        return self.status

    def show_status(self):

        print("\nSystem Status:\n")

        for key, value in self.status.items():

            print(f"{key}: {value}")