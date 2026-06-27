from logs.logger import logger


class DocumentAgent:

    def __init__(self):

        self.name = "Document Agent"

        self.capabilities = [
            "read_document",
            "analyze_document",
            "summarize_document",
            "extract_information",
            "compare_documents",
            "generate_report"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "summary" in task_lower:

            result = "Document summarization task accepted."

        elif "extract" in task_lower:

            result = "Information extraction task accepted."

        elif "compare" in task_lower:

            result = "Document comparison task accepted."

        elif "report" in task_lower:

            result = "Report generation task accepted."

        elif "analyze" in task_lower:

            result = "Document analysis task accepted."

        else:

            result = "Document processing task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nDocument Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )