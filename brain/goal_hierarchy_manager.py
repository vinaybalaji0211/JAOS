from logs.logger import logger


class GoalHierarchyManager:

    def __init__(self):
        self.hierarchy = {}

    def add_goal(self, goal):
        self.hierarchy[goal] = {}
        logger.info(f"Goal created: {goal}")

    def add_subgoal(self, goal, subgoal):
        if goal not in self.hierarchy:
            self.hierarchy[goal] = {}

        self.hierarchy[goal][subgoal] = []
        logger.info(f"Subgoal added: {subgoal}")

    def add_task(self, goal, subgoal, task):
        if goal not in self.hierarchy:
            self.hierarchy[goal] = {}

        if subgoal not in self.hierarchy[goal]:
            self.hierarchy[goal][subgoal] = []

        self.hierarchy[goal][subgoal].append(task)
        logger.info(f"Task added: {task}")

    def show_hierarchy(self):
        print("\nGoal Hierarchy:\n")

        if not self.hierarchy:
            print("No goals.")
            return

        for goal, subgoals in self.hierarchy.items():
            print(f"Goal: {goal}")

            for subgoal, tasks in subgoals.items():
                print(f"  Subgoal: {subgoal}")

                for task in tasks:
                    print(f"    - {task}")