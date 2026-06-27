from logs.logger import logger


class LongTermPlanner:

    def __init__(self):
        self.plans = []

    def add_plan(
            self,
            plan_name,
            time_frame,
            objective):

        plan = {
            "plan_name": plan_name,
            "time_frame": time_frame,
            "objective": objective,
            "status": "PLANNED"
        }

        self.plans.append(plan)

        logger.info(
            f"Long-term plan added: {plan_name}"
        )

    def update_status(
            self,
            plan_name,
            status):

        for plan in self.plans:
            if plan["plan_name"] == plan_name:
                plan["status"] = status

                logger.info(
                    f"Plan status updated: {plan_name}"
                )

    def show_plans(self):

        print("\nLong-Term Planner:\n")

        if not self.plans:
            print("No long-term plans.")
            return

        for index, plan in enumerate(
                self.plans,
                start=1):

            print(
                f"{index}. {plan['plan_name']} | "
                f"{plan['time_frame']} | "
                f"{plan['objective']} | "
                f"{plan['status']}"
            )