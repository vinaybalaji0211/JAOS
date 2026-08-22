from jaos_platform.boot_manager import BootManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.startup_validator import StartupValidator


def test_startup_validator_reports_ready_after_boot():
    runtime = PlatformRuntime()

    assert BootManager(runtime).boot() is True

    report = StartupValidator(runtime).validate()

    assert report["ready"] is True


def test_startup_validator_reports_not_ready_before_start():
    runtime = PlatformRuntime()

    report = StartupValidator(runtime).validate()

    assert report["ready"] is False
    assert report["lifecycle_ready"] is False


def test_lifecycle_ready_reflects_runtime_lifecycle_state():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    report = StartupValidator(runtime).validate()

    assert report["lifecycle_ready"] is True
    assert runtime.lifecycle_state == RuntimeLifecycleState.READY


def test_runtime_integrity_delegates_to_runtime_validator():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    report = StartupValidator(runtime).validate()

    assert report["runtime_integrity"] is True


def test_dependencies_satisfied_delegates_to_dependency_validator():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    report = StartupValidator(runtime).validate()

    assert report["dependencies_satisfied"] is True
