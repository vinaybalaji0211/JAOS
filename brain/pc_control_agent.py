from logs.logger import logger


class PCControlAgent:

    def __init__(self):

        self.name = "PC Control Agent"

        self.capabilities = [
            "launch_application",
            "close_application",
            "monitor_system",
            "manage_files",
            "execute_workflow",
            "system_control"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "launch" in task_lower:

            result = "Application launch task accepted."

        elif "close" in task_lower:

            result = "Application close task accepted."

        elif "file" in task_lower:

            result = "File management task accepted."

        elif "monitor" in task_lower:

            result = "System monitoring task accepted."

        elif "workflow" in task_lower:

            result = "Workflow execution task accepted."

        else:

            result = "General PC control task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nPC Control Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )