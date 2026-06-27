from logs.logger import logger


class GoalHierarchyEngine:

    def __init__(self):

        self.goals = []

    def add_goal(
            self,
            goal,
            priority=1,
            status="ACTIVE",
            parent=None):

        self.goals.append(

            {
                "goal": goal,
                "priority": priority,
                "status": status,
                "parent": parent
            }

        )

        logger.info(
            f"Goal added: {goal}"
        )

    def show_goals(self):

        print("\nGoal Hierarchy:\n")

        goals = sorted(

            self.goals,

            key=lambda item: item["priority"]

        )

        for goal in goals:

            print(

                f"Goal: {goal['goal']}"

            )

            print(

                f"Priority: {goal['priority']}"

            )

            print(

                f"Status: {goal['status']}"

            )

            print(

                f"Parent Goal: {goal['parent']}"

            )

            print()