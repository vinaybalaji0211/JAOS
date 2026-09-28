from executive_brain.brain.executive_brain import ExecutiveBrain
from executive_brain.memory.memory_manager import MemoryManager
from workflow.workflow_engine import WorkflowEngine


class ExecutivePipeline:
    """Primary execution pipeline for JAOS."""

    def __init__(self):
        self.executive_brain = ExecutiveBrain()
        self.executive_brain.initialize()

        self.memory = MemoryManager()
        self.workflow = WorkflowEngine()

    def execute(self, user_request: str) -> dict:
        self.memory.set_user_request(user_request)

        response = {
            "request": user_request,
            "brain": self.executive_brain.get_status(),
            "memory": self.memory.get_status(),
            "workflow": "READY",
            "result": "PIPELINE_EXECUTED",
        }

        return response