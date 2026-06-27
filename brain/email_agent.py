from logs.logger import logger


class EmailAgent:

    def __init__(self):

        self.name = "Email Agent"

        self.capabilities = [
            "read_email",
            "draft_email",
            "summarize_email",
            "categorize_email",
            "detect_priority",
            "manage_workflow"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "draft" in task_lower:

            result = "Email drafting task accepted."

        elif "summary" in task_lower:

            result = "Email summarization task accepted."

        elif "priority" in task_lower:

            result = "Priority detection task accepted."

        elif "categorize" in task_lower:

            result = "Email categorization task accepted."

        elif "read" in task_lower:

            result = "Email reading task accepted."

        else:

            result = "General email task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nEmail Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )