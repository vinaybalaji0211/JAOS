import json
import os
from datetime import datetime

from logs.logger import logger


class GoalTracker:

    FILE_PATH = "data/goals/goals.json"

    @staticmethod
    def add_goal(goal):

        os.makedirs(
            "data/goals",
            exist_ok=True
        )

        goals = GoalTracker.get_goals()

        goals.append(
            {
                "goal": goal,
                "status": "ACTIVE",
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        )

        with open(
                GoalTracker.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                goals,
                file,
                indent=4
            )

        logger.info(
            f"Goal added: {goal}"
        )

    @staticmethod
    def get_goals():

        if not os.path.exists(
                GoalTracker.FILE_PATH):

            return []

        with open(
                GoalTracker.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            try:

                return json.load(file)

            except:

                return []

    @staticmethod
    def show_goals():

        goals = GoalTracker.get_goals()

        print("\nGoals:")

        if not goals:

            print("No goals found.")

        else:

            for index, goal in enumerate(
                    goals,
                    start=1):

                print(
                    f"{index}. {goal['goal']} - {goal['status']}"
                )