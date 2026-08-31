from jaos_platform.platform_runtime import PlatformRuntime
from workflow.workflow_engine import WorkflowEngine


def test_workflow_registers_with_runtime():
    runtime = PlatformRuntime()

    workflow = WorkflowEngine(runtime)

    assert runtime.container.resolve("workflow_engine") is workflow


def test_workflow_updates_runtime_context():
    runtime = PlatformRuntime()

    WorkflowEngine(runtime)

    assert runtime.context.get("workflow_engine_status") == "READY"


def test_workflow_registration_still_works():
    runtime = PlatformRuntime()

    workflow = WorkflowEngine(runtime)
    workflow.register_workflow("test_flow")

    assert workflow.workflow_status("test_flow") == "READY"