from logs.logger import logger


class SelfUpgradePlanner:

    def __init__(self):

        self.plans = {}

    def create_plan(
            self,
            upgrade_name,
            steps):

        self.plans[
            upgrade_name
        ] = steps

        logger.info(
            f"Upgrade plan created: "
            f"{upgrade_name}"
        )

    def show_plan(
            self,
            upgrade_name):

        print(
            f"\nUpgrade Plan: "
            f"{upgrade_name}\n"
        )

        steps = self.plans.get(
            upgrade_name,
            []
        )

        if not steps:

            print(
                "No plan found."
            )

            return

        for index, step in enumerate(
                steps,
                start=1):

            print(
                f"{index}. {step}"
            )