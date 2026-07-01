from executive_brain.brain.executive_brain import ExecutiveBrain
from executive_brain.memory.memory_manager import MemoryManager
from jaos_platform.platform_runtime import PlatformRuntime


def test_memory_manager_registers_with_runtime():
    runtime = PlatformRuntime()

    memory = MemoryManager(runtime)

    assert runtime.container.resolve("memory_manager") is memory


def test_memory_manager_updates_runtime_context():
    runtime = PlatformRuntime()

    MemoryManager(runtime)

    assert runtime.context.get("memory_manager_status") == "READY"


def test_executive_uses_runtime_memory_manager():
    runtime = PlatformRuntime()

    memory = MemoryManager(runtime)
    brain = ExecutiveBrain(runtime)

    assert brain.get_memory_manager() is memory


def test_executive_creates_memory_manager_when_missing():
    runtime = PlatformRuntime()

    brain = ExecutiveBrain(runtime)

    assert runtime.container.resolve("memory_manager") is brain.get_memory_manager()