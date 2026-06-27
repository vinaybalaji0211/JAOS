from logs.logger import logger


class WorkflowEngine:

    def __init__(self):

        self.workflows = {}

    def register_workflow(
            self,
            workflow_name,
            status="READY"):

        self.workflows[workflow_name] = status

        logger.info(
            f"Workflow registered: {workflow_name}"
        )

    def workflow_status(
            self,
            workflow_name):

        return self.workflows.get(
            workflow_name,
            "UNKNOWN"
        )

    def show_workflows(self):

        print("\n=== Workflow Engine ===\n")

        if not self.workflows:

            print("No workflows registered.")
            return

        for workflow, status in self.workflows.items():

            print(
                f"{workflow}: {status}"
            )