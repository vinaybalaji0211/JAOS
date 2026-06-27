from workflow.workflow_engine import (
    WorkflowEngine
)

engine = WorkflowEngine()

engine.register_workflow(
    "Morning Briefing"
)

engine.register_workflow(
    "GitHub Automation"
)

engine.register_workflow(
    "Research Workflow"
)

engine.show_workflows()

print(
    "\nStatus:",
    engine.workflow_status(
        "GitHub Automation"
    )
)