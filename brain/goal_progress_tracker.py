from logs.logger import logger


class GoalProgressTracker:

    def __init__(self):
        self.goals = {}

    def add_goal(self, goal_name):
        self.goals[goal_name] = {
            "progress": 0,
            "milestones": [],
            "status_history": ["CREATED"],
            "completed": False
        }

        logger.info(f"Goal tracking started: {goal_name}")

    def add_milestone(self, goal_name, milestone):
        if goal_name in self.goals:
            self.goals[goal_name]["milestones"].append(
                milestone
            )

            logger.info(f"Milestone added: {milestone}")

    def update_progress(self, goal_name, progress):
        if goal_name in self.goals:
            self.goals[goal_name]["progress"] = progress
            self.goals[goal_name]["status_history"].append(
                f"PROGRESS_UPDATED_TO_{progress}%"
            )

            if progress >= 100:
                self.goals[goal_name]["completed"] = True
                self.goals[goal_name]["status_history"].append(
                    "COMPLETED"
                )

            logger.info(f"Progress updated: {goal_name}")

    def show_progress(self):
        print("\nGoal Progress Tracker:\n")

        if not self.goals:
            print("No goals tracked.")
            return

        for goal, details in self.goals.items():
            print(f"Goal: {goal}")
            print(f"Progress: {details['progress']}%")
            print(f"Completed: {details['completed']}")
            print(f"Milestones: {details['milestones']}")
            print(f"History: {details['status_history']}")
            print()