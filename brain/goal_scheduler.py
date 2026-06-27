from logs.logger import logger


class GoalScheduler:

    def __init__(self):

        self.goals = []

    def schedule_goal(
            self,
            goal_name,
            schedule,
            priority=1):

        goal = {
            "goal_name": goal_name,
            "schedule": schedule,
            "priority": priority,
            "status": "ACTIVE"
        }

        self.goals.append(goal)

        logger.info(
            f"Goal scheduled: {goal_name}"
        )

    def complete_goal(
            self,
            goal_name):

        for goal in self.goals:

            if goal["goal_name"] == goal_name:

                goal["status"] = "COMPLETED"

                logger.info(
                    f"Goal completed: {goal_name}"
                )

    def show_goals(self):

        print("\nGoal Scheduler:\n")

        if not self.goals:

            print("No scheduled goals.")

            return

        for index, goal in enumerate(
                self.goals,
                start=1):

            print(
                f"{index}. {goal['goal_name']} | "
                f"{goal['schedule']} | "
                f"Priority={goal['priority']} | "
                f"{goal['status']}"
            )