from logs.logger import logger


class StrategicPlanningEngine:

    def __init__(self):

        self.plans = []

    def create_plan(
            self,
            goal,
            milestones):

        plan = {
            "goal": goal,
            "milestones": milestones,
            "status": "ACTIVE"
        }

        self.plans.append(
            plan
        )

        logger.info(
            f"Strategic plan created: "
            f"{goal}"
        )

    def complete_plan(
            self,
            goal):

        for plan in self.plans:

            if plan["goal"] == goal:

                plan["status"] = "COMPLETED"

                logger.info(
                    f"Plan completed: "
                    f"{goal}"
                )

    def show_plans(self):

        print(
            "\nStrategic Planning Engine:\n"
        )

        if not self.plans:

            print(
                "No strategic plans."
            )

            return

        for plan in self.plans:

            print(
                f"Goal: {plan['goal']}"
            )

            print(
                f"Status: {plan['status']}"
            )

            print(
                "Milestones:"
            )

            for milestone in (
                    plan["milestones"]):

                print(
                    f" - {milestone}"
                )

            print()