from logs.logger import logger


class WorkflowMonitor:

    def __init__(self):

        self.workflows = {}

    def update_workflow(
            self,
            workflow_name,
            status):

        self.workflows[workflow_name] = status

        logger.info(
            f"Workflow updated: {workflow_name}"
        )

    def show_workflows(self):

        print(
            "\n=== Workflow Monitor ===\n"
        )

        if not self.workflows:

            print(
                "No active workflows."
            )

            return

        for workflow, status in (
                self.workflows.items()):

            print(
                f"{workflow}"
            )

            print(
                f"  Status : {status}"
            )

            print()