from jaos_platform.boot_manager import BootManager
from jaos_platform.platform_runtime import PlatformRuntime


def test_boot_manager_accepts_runtime():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)

    assert manager.runtime is runtime


def test_boot_updates_context():
    runtime = PlatformRuntime()

    runtime.context.set("config_manager_status", "READY")
    runtime.context.set("executive_brain_status", "READY")
    runtime.context.set("startup_manager_status", "READY")

    manager = BootManager(runtime)

    manager.boot()

    assert runtime.context.get("boot_status") == "READY"


def test_boot_registers_all_steps():
    runtime = PlatformRuntime()

    runtime.context.set("config_manager_status", "READY")
    runtime.context.set("executive_brain_status", "READY")
    runtime.context.set("startup_manager_status", "READY")

    manager = BootManager(runtime)

    manager.boot()

    assert manager.steps == [
        "platform_runtime",
        "runtime_validator",
        "startup_validator",
        "dependency_validator",
        "runtime_health_certifier",
    ]


def test_shutdown_updates_context():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)

    manager.shutdown()

    assert runtime.context.get("boot_status") == "SHUTDOWN"