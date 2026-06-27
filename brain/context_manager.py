from logs.logger import logger


class ContextManager:

    def __init__(self):
        self.context = {
            "current_goal": None,
            "current_task": None,
            "current_user_request": None,
            "current_agent": None,
            "current_mode": "NORMAL",
            "recent_context": []
        }

    def update_context(
            self,
            key,
            value):

        if key in self.context:
            self.context[key] = value
            logger.info(f"Context updated: {key}")

    def add_recent_context(
            self,
            item):

        self.context["recent_context"].append(item)

        if len(self.context["recent_context"]) > 5:
            self.context["recent_context"].pop(0)

        logger.info("Recent context added.")

    def show_context(self):

        print("\nContext Manager:\n")

        for key, value in self.context.items():
            print(f"{key}: {value}")