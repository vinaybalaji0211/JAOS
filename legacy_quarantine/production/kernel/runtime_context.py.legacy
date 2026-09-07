from datetime import datetime

from logs.logger import logger


class RuntimeContext:

    def __init__(self):

        self.context = {
            "session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "current_user": None,
            "active_ai_provider": None,
            "active_agent": None,
            "active_workflow": None,
            "active_project": None,
            "current_mode": "DESKTOP",
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def update_context(self, key, value):

        self.context[key] = value

        logger.info(
            f"Runtime context updated: {key}"
        )

    def get_context(self, key):

        return self.context.get(key)

    def show_context(self):

        print("\n========== RUNTIME CONTEXT ==========\n")

        for key, value in self.context.items():

            print(f"{key}: {value}")