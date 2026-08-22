"""FORTRESS-03J closure evidence.

One consolidated, explicitly-named test per required FORTRESS-03 lifecycle
invariant. Several of these invariants are already exercised piecewise by
test_platform_runtime_lifecycle.py, test_boot_manager.py,
test_startup_validator.py, test_runtime_health_certifier.py, and
test_event_bus.py; this file is the single place that names each required
invariant directly against a live object graph, for closure evidence.
"""

from __future__ import annotations

import pytest

from jaos_platform.boot_manager import BootManager
from jaos_platform.health_status import HealthStatus
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.lifecycle_transitions import LifecycleTransitionError
from jaos_platform.platform_runtime import PartialShutdownError, PlatformRuntime
from jaos_platform.runtime_health_certifier import RuntimeHealthCertifier
from jaos_platform.startup_validator import StartupValidator

from run_jaos import JAOSApplication


def test_construction_is_not_readiness():
    runtime = PlatformRuntime()

    assert runtime.lifecycle_state == RuntimeLifecycleState.CREATED
    assert StartupValidator(runtime).validate()["ready"] is False


def test_ready_only_after_required_readiness(monkeypatch):
    healthy_runtime = PlatformRuntime()
    assert BootManager(healthy_runtime).boot() is True
    assert healthy_runtime.lifecycle_state == RuntimeLifecycleState.READY
    assert StartupValidator(healthy_runtime).validate()["ready"] is True

    unready_runtime = PlatformRuntime()
    monkeypatch.setattr(
        StartupValidator,
        "validate",
        lambda self: {"ready": False, "lifecycle_ready": False},
    )
    assert BootManager(unready_runtime).boot() is False
    assert unready_runtime.lifecycle_state != RuntimeLifecycleState.READY
    assert unready_runtime.lifecycle_state == RuntimeLifecycleState.FAILED


def test_invalid_transitions_fail():
    runtime = PlatformRuntime()

    with pytest.raises(LifecycleTransitionError):
        runtime.start()

    with pytest.raises(LifecycleTransitionError):
        runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.CREATED


def test_partial_startup_rollback():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.container.register("event_bus", object())

    with pytest.raises(ValueError):
        runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED
    assert runtime.container.is_registered("service_container") is False
    assert runtime.container.is_registered("service_registry") is False
    assert runtime.container.is_registered("runtime_context") is False
    assert runtime.registry.list() == []


def test_reverse_teardown():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED
    assert runtime.container.list_services() == []
    assert runtime.registry.list() == []


def test_shutdown_continues_through_failures(monkeypatch):
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    original_unregister = runtime.registry.unregister

    def broken_unregister(name):
        if name == "service_registry":
            raise RuntimeError("registry unregister exploded")
        return original_unregister(name)

    monkeypatch.setattr(runtime.registry, "unregister", broken_unregister)

    with pytest.raises(PartialShutdownError):
        runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED
    assert runtime.container.is_registered("event_bus") is False
    assert runtime.container.is_registered("runtime_context") is False
    assert runtime.container.is_registered("service_container") is False


def test_truthful_health():
    runtime = PlatformRuntime()
    certifier = RuntimeHealthCertifier(runtime)

    assert certifier.certify() == {"overall": HealthStatus.UNKNOWN}

    runtime.initialize()
    runtime.start()

    assert certifier.certify()["overall"] == HealthStatus.HEALTHY

    runtime.context = None

    assert certifier.certify()["overall"] == HealthStatus.FAILED


def test_degraded_reachable():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    runtime.mark_degraded()
    assert runtime.lifecycle_state == RuntimeLifecycleState.DEGRADED

    runtime.mark_recovered()
    assert runtime.lifecycle_state == RuntimeLifecycleState.READY


def test_no_canonical_legacy_readiness_keys():
    with_legacy_keys = PlatformRuntime()
    with_legacy_keys.context.set("config_manager_status", "READY")
    with_legacy_keys.context.set("executive_brain_status", "READY")
    with_legacy_keys.context.set("startup_manager_status", "READY")
    with_legacy_keys.context.set("boot_status", "READY")

    without_legacy_keys = PlatformRuntime()

    assert (
        StartupValidator(with_legacy_keys).validate()
        == StartupValidator(without_legacy_keys).validate()
    )


def test_production_path_makes_no_fabricated_readiness_claim(capsys):
    JAOSApplication().boot()

    output = capsys.readouterr().out

    assert "Boot Complete" not in output
    assert "Ready" not in output


def test_no_contradictory_runtime_context_lifecycle_facts(monkeypatch):
    runtime = PlatformRuntime()
    monkeypatch.setattr(
        StartupValidator,
        "validate",
        lambda self: {"ready": False, "lifecycle_ready": False},
    )

    BootManager(runtime).boot()

    assert runtime.context.get("boot_status") == runtime.lifecycle_state.value

    stoppable_runtime = PlatformRuntime()
    manager = BootManager(stoppable_runtime)
    manager.boot()
    manager.shutdown()

    assert stoppable_runtime.context.contains("runtime_report") is False
    assert stoppable_runtime.context.contains("startup_report") is False
    assert stoppable_runtime.context.contains("dependency_report") is False
    assert stoppable_runtime.context.contains("health_report") is False
    assert (
        stoppable_runtime.context.get("boot_status")
        == stoppable_runtime.lifecycle_state.value
    )
