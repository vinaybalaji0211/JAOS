from jaos_platform.platform_runtime import PlatformRuntime
from system_services.startup_manager import StartupManager


def test_startup_manager_registers_with_runtime():
    runtime = PlatformRuntime()

    manager = StartupManager(runtime)

    assert runtime.container.resolve("startup_manager") is manager


def test_startup_manager_updates_runtime_context():
    runtime = PlatformRuntime()

    StartupManager(runtime)

    assert (
        runtime.context.get("startup_manager_status")
        == "READY"
    )


def test_startup_service_registration_still_works():
    runtime = PlatformRuntime()

    manager = StartupManager(runtime)

    manager.register_service(
        "ExecutiveBrain",
        True,
    )

    assert manager.services["ExecutiveBrain"] is True