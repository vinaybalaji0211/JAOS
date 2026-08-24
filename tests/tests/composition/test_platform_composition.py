"""FORTRESS-05A/05B: canonical whole-system platform composition."""

from __future__ import annotations

import pytest

from jaos.ai import AIManager
from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.composition import (
    CompositionError,
    CompositionTeardownError,
    PlatformComposition,
)
from jaos.composition.platform_composition import (
    AI_MANAGER_SERVICE,
    EXECUTIVE_CONTROLLER_SERVICE,
    MEMORY_STORE_SERVICE,
    TOOL_MANAGER_SERVICE,
)
from jaos.executive.controller import ExecutiveController
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos.tools.tool_manager import ToolManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths


def _started_runtime(runtime_paths: RuntimePaths) -> PlatformRuntime:
    runtime = PlatformRuntime(runtime_paths=runtime_paths)
    runtime.initialize()
    runtime.start()
    return runtime


def test_compose_registers_real_platforms(jaos_runtime_paths: RuntimePaths):
    runtime = _started_runtime(jaos_runtime_paths)

    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        assert isinstance(composition.tool_manager, ToolManager)
        assert isinstance(composition.ai_manager, AIManager)
        assert isinstance(composition.executive_controller, ExecutiveController)
        assert isinstance(composition.memory_store, SQLiteStore)
        assert composition.tool_manager.list_tools()

        expected = {
            "event_bus",
            "runtime_context",
            "service_container",
            "service_registry",
            TOOL_MANAGER_SERVICE,
            AI_MANAGER_SERVICE,
            EXECUTIVE_CONTROLLER_SERVICE,
            MEMORY_STORE_SERVICE,
        }
        assert set(runtime.container.list_services()) == expected
        assert set(runtime.registry.list()) == expected
    finally:
        composition.teardown()


def test_dependency_injection_identity_flows_to_command_dispatcher(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    assert runtime.container.resolve(TOOL_MANAGER_SERVICE) is composition.tool_manager
    assert runtime.container.resolve(AI_MANAGER_SERVICE) is composition.ai_manager
    assert (
        runtime.container.resolve(EXECUTIVE_CONTROLLER_SERVICE)
        is composition.executive_controller
    )

    dispatcher = CommandDispatcher(
        composition.tool_manager,
        ai_manager=composition.ai_manager,
        executive=composition.executive_controller,
    )

    assert dispatcher.tool_manager is composition.tool_manager
    assert dispatcher.ai_manager is composition.ai_manager
    assert dispatcher.executive is composition.executive_controller
    assert dispatcher._owns_ai_manager is False

    composition.teardown()


def test_compose_requires_ready_runtime():
    runtime = PlatformRuntime()

    with pytest.raises(CompositionError, match="CREATED"):
        PlatformComposition(runtime).compose()

    assert runtime.container.list_services() == []


def test_compose_requires_ready_not_stopped_runtime(jaos_runtime_paths: RuntimePaths):
    runtime = _started_runtime(jaos_runtime_paths)
    runtime.stop()

    with pytest.raises(CompositionError, match="STOPPED"):
        PlatformComposition(runtime).compose()


def test_compose_failure_rolls_back_previously_registered_platforms(
    monkeypatch, jaos_runtime_paths: RuntimePaths
):
    runtime = _started_runtime(jaos_runtime_paths)

    import jaos.composition.platform_composition as composition_module

    def broken_executive(*_args, **_kwargs):
        raise RuntimeError("executive construction exploded")

    monkeypatch.setattr(
        composition_module, "ExecutiveController", broken_executive
    )

    composition = PlatformComposition(runtime)

    with pytest.raises(RuntimeError, match="executive construction exploded"):
        composition.compose()

    assert runtime.container.is_registered(TOOL_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(AI_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False
    assert runtime.registry.is_registered(TOOL_MANAGER_SERVICE) is False
    assert runtime.registry.is_registered(AI_MANAGER_SERVICE) is False
    assert runtime.registry.is_registered(MEMORY_STORE_SERVICE) is False
    assert set(runtime.container.list_services()) == {
        "event_bus",
        "runtime_context",
        "service_container",
        "service_registry",
    }
    assert not jaos_runtime_paths.memory.exists()


def test_teardown_releases_composed_platforms(jaos_runtime_paths: RuntimePaths):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    store = composition.memory_store

    composition.teardown()

    assert runtime.container.is_registered(TOOL_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(AI_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(EXECUTIVE_CONTROLLER_SERVICE) is False
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False
    assert runtime.registry.is_registered(MEMORY_STORE_SERVICE) is False
    assert store.is_closed is True


def test_teardown_continues_after_failure_and_aggregates(
    monkeypatch, jaos_runtime_paths: RuntimePaths
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    monkeypatch.setattr(
        composition.ai_manager,
        "shutdown",
        lambda: (_ for _ in ()).throw(RuntimeError("ai shutdown exploded")),
    )

    with pytest.raises(CompositionTeardownError, match="ai shutdown exploded"):
        composition.teardown()

    assert runtime.container.is_registered(TOOL_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(AI_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(EXECUTIVE_CONTROLLER_SERVICE) is False
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False


def test_composed_ai_manager_has_a_healthy_default_provider(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        status = composition.ai_manager.get_diagnostic_status()

        assert status.healthy is True
    finally:
        composition.teardown()
