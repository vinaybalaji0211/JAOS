from logs.logger import logger


class GoalStack:

    def __init__(self):

        self.goals = []

    def add_goal(
            self,
            goal_name,
            priority):

        goal = {

            "goal_name": goal_name,

            "priority": priority

        }

        self.goals.append(
            goal
        )

        self.goals.sort(
            key=lambda x: x["priority"]
        )

        logger.info(
            f"Goal added: {goal_name}"
        )

    def remove_goal(
            self,
            goal_name):

        self.goals = [

            goal

            for goal in self.goals

            if goal["goal_name"] != goal_name

        ]

        logger.info(
            f"Goal removed: {goal_name}"
        )

    def get_current_goal(self):

        if not self.goals:

            return None

        return self.goals[0]

    def show_goals(self):

        print("\nGoal Stack:\n")

        if not self.goals:

            print(
                "No goals."
            )

            return

        for index, goal in enumerate(
                self.goals,
                start=1):

            print(
                f"{index}. "

                f"{goal['goal_name']} "

                f"(Priority {goal['priority']})"
            )