from logs.logger import logger


class PlannerEngine:

    @staticmethod
    def create_plan(intent, goal):

        plan = []

        if intent == "TASK":

            plan = [
                "Understand the task",
                "Break task into smaller steps",
                "Check required capabilities",
                "Validate safety",
                "Prepare execution plan"
            ]

        elif intent == "QUESTION":

            plan = [
                "Understand the question",
                "Search memory for related information",
                "Prepare answer"
            ]

        elif intent == "MEMORY":

            plan = [
                "Identify memory operation",
                "Check memory safety",
                "Store or retrieve memory"
            ]

        elif intent == "SYSTEM":

            plan = [
                "Check system status",
                "Collect diagnostics",
                "Report system state"
            ]

        elif intent == "RESEARCH":

            plan = [
                "Define research topic",
                "Search available knowledge",
                "Summarize findings"
            ]

        elif intent == "FILE":

            plan = [
                "Identify file operation",
                "Check permissions",
                "Perform safe file action"
            ]

        else:

            plan = [
                "Clarify user request",
                "Ask for missing details"
            ]

        logger.info(
            f"Plan created for intent: {intent}"
        )

        return {
            "intent": intent,
            "goal": goal,
            "plan": plan
        }

    @staticmethod
    def show_plan(intent, goal):

        result = PlannerEngine.create_plan(
            intent,
            goal
        )

        print("\nPlanner Engine Output:")

        print(
            f"Intent: {result['intent']}"
        )

        print(
            f"Goal: {result['goal']}"
        )

        print("\nPlan:")

        for index, step in enumerate(
                result["plan"],
                start=1):

            print(
                f"{index}. {step}"
            )