from logs.logger import logger


class DigitalTwin:

    @staticmethod
    def simulate(
            plan_steps,
            resources_ok,
            risk_level,
            prediction_count,
            confidence):

        if not plan_steps:

            result = "NOT_FEASIBLE"

        elif not resources_ok:

            result = "NEEDS_ADJUSTMENT"

        elif risk_level == "HIGH":

            result = "HIGH_RISK"

        elif confidence < 60 or prediction_count > 3:

            result = "NEEDS_ADJUSTMENT"

        else:

            result = "SAFE_TO_EXECUTE"

        logger.info(
            f"Digital twin simulation result: {result}"
        )

        return result

    @staticmethod
    def show_simulation(
            plan_steps,
            resources_ok,
            risk_level,
            prediction_count,
            confidence):

        result = DigitalTwin.simulate(
            plan_steps,
            resources_ok,
            risk_level,
            prediction_count,
            confidence
        )

        print("\nDigital Twin Simulation:\n")

        print(
            f"Plan Steps: {len(plan_steps)}"
        )

        print(
            f"Resources OK: {resources_ok}"
        )

        print(
            f"Risk Level: {risk_level}"
        )

        print(
            f"Prediction Count: {prediction_count}"
        )

        print(
            f"Confidence: {confidence}"
        )

        print(
            f"\nSimulation Result: {result}"
        )