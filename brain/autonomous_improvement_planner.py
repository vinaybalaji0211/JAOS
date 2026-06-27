from logs.logger import logger


class AutonomousImprovementPlanner:

    @staticmethod
    def plan(
            repeated_failures,
            missing_capabilities,
            curiosity_questions):

        improvements = []

        for failure in repeated_failures:

            improvements.append(

                f"Resolve recurring problem: {failure}"

            )

        for capability in missing_capabilities:

            improvements.append(

                f"Develop capability: {capability}"

            )

        for question in curiosity_questions:

            improvements.append(

                f"Research: {question}"

            )

        logger.info(
            "Autonomous improvement plan generated."
        )

        return improvements

    @staticmethod
    def show_plan(
            repeated_failures,
            missing_capabilities,
            curiosity_questions):

        plan = (
            AutonomousImprovementPlanner.plan(

                repeated_failures,

                missing_capabilities,

                curiosity_questions

            )
        )

        print("\nAutonomous Improvement Plan:\n")

        if not plan:

            print(
                "No improvements required."
            )

            return

        for index, item in enumerate(
                plan,
                start=1):

            print(
                f"{index}. {item}"
            )