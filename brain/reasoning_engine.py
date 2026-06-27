from logs.logger import logger


class ReasoningEngine:

    @staticmethod
    def reason(plan_data):

        intent = plan_data["intent"]

        goal = plan_data["goal"]

        plan = plan_data["plan"]

        reasoning = []

        reasoning.append(

            f"Detected intent: {intent}"

        )

        reasoning.append(

            f"Goal identified: {goal}"

        )

        reasoning.append(

            f"Plan contains {len(plan)} steps"

        )

        reasoning.append(

            "Execution should only proceed after validation"

        )

        logger.info(

            "Reasoning completed"

        )

        return reasoning

    @staticmethod
    def show_reasoning(plan_data):

        reasoning = (

            ReasoningEngine.reason(

                plan_data

            )

        )

        print(

            "\nReasoning Engine Output:"

        )

        for index, item in enumerate(

                reasoning,

                start=1):

            print(

                f"{index}. {item}"

            )