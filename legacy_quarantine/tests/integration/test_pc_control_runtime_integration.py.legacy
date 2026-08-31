from jaos_platform.platform_runtime import PlatformRuntime
from pc_control.application_manager import ApplicationManager


def test_application_manager_registers_with_runtime():
    runtime = PlatformRuntime()

    manager = ApplicationManager(runtime)

    assert runtime.container.resolve("application_manager") is manager


def test_application_manager_updates_runtime_context():
    runtime = PlatformRuntime()

    ApplicationManager(runtime)

    assert runtime.context.get("application_manager_status") == "READY"


def test_application_registration_still_works():
    runtime = PlatformRuntime()

    manager = ApplicationManager(runtime)
    manager.register_application("notepad", "notepad.exe")

    assert manager.applications["notepad"] == {
        "executable": "notepad.exe",
        "status": "AVAILABLE",
    }