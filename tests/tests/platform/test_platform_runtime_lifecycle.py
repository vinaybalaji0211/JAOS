from pathlib import Path

import pytest

from jaos_platform.boot_manager import BootManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.lifecycle_transitions import LifecycleTransitionError
from jaos_platform.platform_runtime import PartialShutdownError, PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths


def test_construction_state_is_created():
    runtime = PlatformRuntime()

    assert runtime.lifecycle_state == RuntimeLifecycleState.CREATED


def test_construction_registers_zero_platform_services():
    runtime = PlatformRuntime()

    assert runtime.container.list_services() == []
    assert runtime.registry.list() == []


def test_construction_makes_no_readiness_claim():
    runtime = PlatformRuntime()

    assert runtime.context.keys() == []


def test_initialize_reaches_initialized():
    runtime = PlatformRuntime()

    runtime.initialize()

    assert runtime.lifecycle_state == RuntimeLifecycleState.INITIALIZED


def test_start_reaches_ready():
    runtime = PlatformRuntime()
    runtime.initialize()

    runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.READY


def test_platform_services_appear_only_after_start():
    runtime = PlatformRuntime()
    runtime.initialize()

    assert runtime.container.list_services() == []
    assert runtime.registry.list() == []

    runtime.start()

    expected = [
        "event_bus",
        "runtime_context",
        "service_container",
        "service_registry",
    ]
    assert runtime.container.list_services() == expected
    assert runtime.registry.list() == expected


def test_stop_tears_down_platform_services_in_reverse_order(monkeypatch):
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    container_order = []
    registry_order = []
    original_container_unregister = runtime.container.unregister
    original_registry_unregister = runtime.registry.unregister

    def spy_container_unregister(name):
        container_order.append(name)
        return original_container_unregister(name)

    def spy_registry_unregister(name):
        registry_order.append(name)
        return original_registry_unregister(name)

    monkeypatch.setattr(
        runtime.container, "unregister", spy_container_unregister
    )
    monkeypatch.setattr(
        runtime.registry, "unregister", spy_registry_unregister
    )

    runtime.stop()

    expected_reverse = [
        "event_bus",
        "runtime_context",
        "service_registry",
        "service_container",
    ]
    assert container_order == expected_reverse
    assert registry_order == expected_reverse
    assert runtime.container.list_services() == []
    assert runtime.registry.list() == []
    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED


def test_stopped_is_terminal_for_platform_runtime():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()
    runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED

    with pytest.raises(LifecycleTransitionError):
        runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.STOPPED


def test_start_before_initialize_raises():
    runtime = PlatformRuntime()

    with pytest.raises(LifecycleTransitionError):
        runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.CREATED
    assert runtime.container.list_services() == []


def test_initialize_twice_raises():
    runtime = PlatformRuntime()
    runtime.initialize()

    with pytest.raises(LifecycleTransitionError):
        runtime.initialize()

    assert runtime.lifecycle_state == RuntimeLifecycleState.INITIALIZED


def test_start_twice_raises():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    with pytest.raises(LifecycleTransitionError):
        runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.READY
    assert runtime.container.list_services() == [
        "event_bus",
        "runtime_context",
        "service_container",
        "service_registry",
    ]


def test_start_failure_rolls_back_and_transitions_to_failed():
    runtime = PlatformRuntime()
    runtime.initialize()

    sentinel = object()
    runtime.container.register("event_bus", sentinel)

    with pytest.raises(ValueError):
        runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED

    assert runtime.container.is_registered("service_container") is False
    assert runtime.container.is_registered("service_registry") is False
    assert runtime.container.is_registered("runtime_context") is False
    assert runtime.container.resolve("event_bus") is sentinel

    assert runtime.registry.is_registered("service_container") is False
    assert runtime.registry.is_registered("service_registry") is False
    assert runtime.registry.is_registered("runtime_context") is False
    assert runtime.registry.is_registered("event_bus") is False


def test_start_failure_unwinds_only_previously_started_components_in_reverse_order(
    monkeypatch,
):
    runtime = PlatformRuntime()
    runtime.initialize()

    sentinel = object()
    runtime.container.register("runtime_context", sentinel)

    container_order = []
    registry_order = []
    original_container_unregister = runtime.container.unregister
    original_registry_unregister = runtime.registry.unregister

    def spy_container_unregister(name):
        container_order.append(name)
        return original_container_unregister(name)

    def spy_registry_unregister(name):
        registry_order.append(name)
        return original_registry_unregister(name)

    monkeypatch.setattr(
        runtime.container, "unregister", spy_container_unregister
    )
    monkeypatch.setattr(
        runtime.registry, "unregister", spy_registry_unregister
    )

    with pytest.raises(ValueError):
        runtime.start()

    assert container_order == ["service_registry", "service_container"]
    assert registry_order == ["service_registry", "service_container"]
    assert runtime.container.is_registered("service_container") is False
    assert runtime.container.is_registered("service_registry") is False
    assert runtime.container.resolve("runtime_context") is sentinel
    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED


def test_start_failure_preserves_original_failure_as_observable(monkeypatch):
    runtime = PlatformRuntime()
    runtime.initialize()

    runtime.container.register("event_bus", object())

    with pytest.raises(ValueError, match="event_bus"):
        runtime.start()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED


def test_boot_completed_subscriber_failure_does_not_corrupt_boot_result():
    runtime = PlatformRuntime()

    def broken_subscriber(_payload):
        raise RuntimeError("subscriber exploded")

    runtime.events.subscribe("boot_completed", broken_subscriber)

    manager = BootManager(runtime)

    assert manager.boot() is True
    assert runtime.lifecycle_state == RuntimeLifecycleState.READY
    assert manager.status == "READY"


def test_stop_continues_after_individual_component_failure_and_aggregates_errors(
    monkeypatch,
):
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    original_registry_unregister = runtime.registry.unregister

    def broken_registry_unregister(name):
        if name == "runtime_context":
            raise RuntimeError("registry unregister exploded")
        return original_registry_unregister(name)

    monkeypatch.setattr(
        runtime.registry, "unregister", broken_registry_unregister
    )

    with pytest.raises(PartialShutdownError, match="runtime_context"):
        runtime.stop()

    assert runtime.lifecycle_state == RuntimeLifecycleState.FAILED

    assert runtime.container.is_registered("event_bus") is False
    assert runtime.container.is_registered("runtime_context") is False
    assert runtime.container.is_registered("service_registry") is False
    assert runtime.container.is_registered("service_container") is False

    assert runtime.registry.is_registered("event_bus") is False
    assert runtime.registry.is_registered("service_registry") is False
    assert runtime.registry.is_registered("service_container") is False
    assert runtime.registry.is_registered("runtime_context") is True


def test_runtime_paths_preserved_across_lifecycle(tmp_path: Path) -> None:
    paths = RuntimePaths(tmp_path / "runtime")
    runtime = PlatformRuntime(runtime_paths=paths)

    assert runtime.runtime_paths is paths
    assert runtime.lifecycle_state == RuntimeLifecycleState.CREATED

    runtime.initialize()
    runtime.start()

    assert runtime.runtime_paths is paths
    assert runtime.context.runtime_paths is paths
