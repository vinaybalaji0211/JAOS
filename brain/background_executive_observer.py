from logs.logger import logger


class BackgroundExecutiveObserver:

    def __init__(self):
        self.observations = {
            "current_goals": [],
            "pending_tasks": [],
            "system_status": "UNKNOWN",
            "security_status": "UNKNOWN",
            "plugin_status": "UNKNOWN",
            "recent_failures": []
        }

    def update_observation(self, key, value):
        if key in self.observations:
            self.observations[key] = value
            logger.info(f"Executive observation updated: {key}")

    def show_observations(self):
        print("\nBackground Executive Observer:\n")

        for key, value in self.observations.items():
            print(f"{key}: {value}")