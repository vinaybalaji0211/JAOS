from logs.logger import logger


class MultiProviderTaskComposer:

    def __init__(self):

        self.execution_plan = []

    def add_step(
            self,
            component,
            action):

        self.execution_plan.append(
            {
                "component": component,
                "action": action
            }
        )

        logger.info(
            f"Execution step added: {component}"
        )

    def show_plan(self):

        print("\n=== Multi-Provider Execution Plan ===\n")

        if not self.execution_plan:

            print("No execution plan.")
            return

        for index, step in enumerate(
                self.execution_plan,
                start=1):

            print(
                f"{index}. "
                f"{step['component']}"
            )

            print(
                f"   Action: "
                f"{step['action']}"
            )

            print()