from logs.logger import logger


class CodingAgent:

    def __init__(self):

        self.name = "Coding Agent"

        self.capabilities = [
            "generate_code",
            "review_code",
            "debug_code",
            "refactor_code",
            "explain_code",
            "create_tests"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "review" in task_lower:

            result = "Code review task accepted."

        elif "debug" in task_lower or "bug" in task_lower:

            result = "Debugging task accepted."

        elif "test" in task_lower:

            result = "Test generation task accepted."

        elif "refactor" in task_lower:

            result = "Refactoring task accepted."

        elif "explain" in task_lower:

            result = "Code explanation task accepted."

        else:

            result = "Code generation task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nCoding Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )