from workflow.automation_rules_engine import AutomationRulesEngine
from workflow.dependency_manager import DependencyManager
from workflow.retry_recovery_engine import RetryRecoveryEngine
from workflow.scheduler import Scheduler
from workflow.task_manager import TaskManager
from workflow.task_queue import TaskQueue
from workflow.workflow_engine import WorkflowEngine
from workflow.workflow_monitor import WorkflowMonitor

print("\n===== WORKFLOW PLATFORM TEST =====\n")

workflow_engine = WorkflowEngine()
workflow_engine.register_workflow("Website Deployment")

task_manager = TaskManager()
task_manager.create_task(
    "Build Website",
    "HIGH"
)

task_queue = TaskQueue()
task_queue.add_task(
    "Build Website",
    "HIGH"
)

scheduler = Scheduler()
scheduler.schedule_task(
    "Daily Report",
    "08:00"
)

dependency_manager = DependencyManager()
dependency_manager.add_dependency(
    "Deploy Website",
    "Run Tests"
)

retry_engine = RetryRecoveryEngine()
retry_engine.register_failure(
    "Deploy Website",
    "GitHub Timeout"
)

automation_engine = AutomationRulesEngine()
automation_engine.add_rule(
    "GitHub Push",
    "Run Tests"
)

workflow_monitor = WorkflowMonitor()
workflow_monitor.update_workflow(
    "Website Deployment",
    "RUNNING"
)

print("\n===== COMPONENT STATUS =====\n")

workflow_engine.show_workflows()
task_manager.show_tasks()
task_queue.show_queue()
scheduler.show_schedule()
dependency_manager.show_dependencies()
retry_engine.show_failures()
automation_engine.show_rules()
workflow_monitor.show_workflows()

print("\n===== WORKFLOW PLATFORM COMPLETE =====")