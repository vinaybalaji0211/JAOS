from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class WorkflowEngine(BasePlatformService):
    """Central workflow orchestration service."""

    SERVICE_NAME = "workflow_engine"

    def __init__(self, runtime=None):
        self.workflows = {}

        super().__init__(runtime)

    def register_workflow(self, workflow_name, status="READY"):
        self.workflows[workflow_name] = status

        logger.info(f"Workflow registered: {workflow_name}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "workflow_registered",
                {
                    "workflow": workflow_name,
                    "status": status,
                },
            )

    def workflow_status(self, workflow_name):
        return self.workflows.get(
            workflow_name,
            "UNKNOWN",
        )

    def show_workflows(self):
        print("\n=== Workflow Engine ===\n")

        if not self.workflows:
            print("No workflows registered.")
            return

        for workflow, status in self.workflows.items():
            print(f"{workflow}: {status}")