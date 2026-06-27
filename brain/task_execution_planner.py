from logs.logger import logger


class TaskExecutionPlanner:

    def __init__(self):

        self.tasks = {}

    def create_plan(
            self,
            goal,
            steps):

        self.tasks[goal] = steps

        logger.info(
            f"Plan created: {goal}"
        )

    def show_plan(
            self,
            goal):

        print(
            f"\nTask Plan: {goal}\n"
        )

        plan = self.tasks.get(
            goal,
            []
        )

        if not plan:

            print(
                "No plan found."
            )

            return

        for index, step in enumerate(
                plan,
                start=1):

            print(
                f"{index}. {step}"
            )