import pytest

from jaos_platform.boot_manager import BootManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.lifecycle_transitions import LifecycleTransitionError
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.startup_validator import StartupValidator


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


def test_boot_returns_true_and_reaches_platform_runtime_ready():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)

    assert manager.boot() is True
    assert runtime.lifecycle_state == RuntimeLifecycleState.READY
    assert manager.status == "READY"


def test_repeated_boot_is_rejected_by_lifecycle_legality():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)
    manager.boot()

    with pytest.raises(LifecycleTransitionError):
        manager.boot()

    assert runtime.lifecycle_state == RuntimeLifecycleState.READY


def test_boot_steps_reset_and_do_not_accumulate_across_attempts():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)
    manager.boot()
    first_attempt_steps = list(manager.steps)

    with pytest.raises(LifecycleTransitionError):
        manager.boot()

    assert manager.steps == []
    assert first_attempt_steps == [
        "platform_runtime",
        "runtime_validator",
        "startup_validator",
        "dependency_validator",
        "runtime_health_certifier",
    ]


def test_required_validation_failure_prevents_ready(monkeypatch):
    runtime = PlatformRuntime()

    monkeypatch.setattr(
        StartupValidator,
        "validate",
        lambda self: {"ready": False, "lifecycle_ready": False},
    )

    manager = BootManager(runtime)

    assert manager.boot() is False
    assert manager.status == "FAILED"
    assert runtime.context.get("boot_status") == "FAILED"
    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED


def test_start_failure_produces_truthful_failed_state():
    runtime = PlatformRuntime()
    runtime.container.register("event_bus", object())

    manager = BootManager(runtime)

    assert manager.boot() is False
    assert manager.status == "FAILED"
    assert runtime.context.get("boot_status") == "FAILED"
    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED
    assert manager.steps == []