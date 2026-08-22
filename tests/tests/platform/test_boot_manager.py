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


def test_shutdown_after_boot_stops_runtime_and_clears_boot_time_context():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)
    manager.boot()

    assert manager.shutdown() is True
    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert manager.status == "STOPPED"
    assert runtime.context.get("boot_status") == "STOPPED"
    assert runtime.context.contains("runtime_report") is False
    assert runtime.context.contains("startup_report") is False
    assert runtime.context.contains("dependency_report") is False
    assert runtime.context.contains("health_report") is False


def test_shutdown_releases_event_subscriptions():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)
    manager.boot()
    runtime.events.subscribe("custom_event", lambda _payload: None)

    manager.shutdown()

    assert runtime.events.subscriber_count("custom_event") == 0
    assert runtime.events.subscriber_count("boot_shutdown") == 0


def test_shutdown_is_idempotent_after_stop():
    runtime = PlatformRuntime()

    manager = BootManager(runtime)
    manager.boot()

    assert manager.shutdown() is True
    assert manager.shutdown() is True
    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert manager.status == "STOPPED"


def test_shutdown_after_failed_boot_does_not_attempt_illegal_transition(
    monkeypatch,
):
    runtime = PlatformRuntime()

    monkeypatch.setattr(
        StartupValidator,
        "validate",
        lambda self: {"ready": False, "lifecycle_ready": False},
    )

    manager = BootManager(runtime)
    manager.boot()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED

    assert manager.shutdown() is True
    assert manager.status == "FAILED"
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