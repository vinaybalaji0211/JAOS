from logs.logger import logger


class GoalManager:

    def __init__(self):
        self.goals = {}

    def add_goal(
            self,
            goal_name,
            priority=1):

        self.goals[goal_name] = {
            "priority": priority,
            "status": "ACTIVE",
            "progress": 0
        }

        logger.info(f"Goal added: {goal_name}")

    def update_status(
            self,
            goal_name,
            status):

        if goal_name in self.goals:
            self.goals[goal_name]["status"] = status
            logger.info(f"Goal status updated: {goal_name}")

    def update_progress(
            self,
            goal_name,
            progress):

        if goal_name in self.goals:
            self.goals[goal_name]["progress"] = progress
            logger.info(f"Goal progress updated: {goal_name}")

    def show_goals(self):

        print("\nGoal Manager:\n")

        if not self.goals:
            print("No goals.")
            return

        sorted_goals = sorted(
            self.goals.items(),
            key=lambda item: item[1]["priority"]
        )

        for name, details in sorted_goals:
            print(
                f"{name} | "
                f"Priority {details['priority']} | "
                f"{details['status']} | "
                f"Progress {details['progress']}%"
            )