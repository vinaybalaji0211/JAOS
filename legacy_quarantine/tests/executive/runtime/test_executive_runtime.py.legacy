from executive_brain.brain.executive_brain import ExecutiveBrain
from jaos_platform.platform_runtime import PlatformRuntime


def test_executive_accepts_runtime():
    runtime = PlatformRuntime()

    brain = ExecutiveBrain(runtime)

    assert brain.runtime is runtime


def test_executive_registered():
    runtime = PlatformRuntime()

    brain = ExecutiveBrain(runtime)

    assert runtime.container.resolve("executive_brain") is brain


def test_context_updated():
    runtime = PlatformRuntime()

    ExecutiveBrain(runtime)

    assert runtime.context.get("executive_brain_status") == "INITIALIZED"


def test_initialize_updates_context():
    runtime = PlatformRuntime()

    brain = ExecutiveBrain(runtime)
    brain.initialize()

    assert runtime.context.get("executive_brain_status") == "READY"