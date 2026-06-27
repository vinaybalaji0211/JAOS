from workflow.workflow_monitor import (
    WorkflowMonitor
)

monitor = WorkflowMonitor()

monitor.update_workflow(
    "Morning Briefing",
    "RUNNING"
)

monitor.update_workflow(
    "Deploy Website",
    "WAITING"
)

monitor.update_workflow(
    "YOLO Training",
    "PAUSED"
)

monitor.show_workflows()