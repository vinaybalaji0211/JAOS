"""FORTRESS-05C: canonical Memory platform composition."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from jaos.composition import PlatformComposition
from jaos.composition.platform_composition import (
    AI_MANAGER_SERVICE,
    EXECUTIVE_CONTROLLER_SERVICE,
    MEMORY_STORE_SERVICE,
    TOOL_MANAGER_SERVICE,
)
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths


def _started_runtime(runtime_paths: RuntimePaths) -> PlatformRuntime:
    runtime = PlatformRuntime(runtime_paths=runtime_paths)
    runtime.initialize()
    runtime.start()
    return runtime


def _find_repository_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "run_jaos.py").is_file():
            return candidate
    raise RuntimeError("run_jaos.py not found above " + str(start))


def test_compose_creates_exactly_one_memory_store_with_matching_identity(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        assert isinstance(composition.memory_store, SQLiteStore)
        assert runtime.container.resolve(MEMORY_STORE_SERVICE) is composition.memory_store
        assert runtime.registry.is_registered(MEMORY_STORE_SERVICE) is True
        assert runtime.registry.get(MEMORY_STORE_SERVICE).name == MEMORY_STORE_SERVICE
    finally:
        composition.teardown()


def test_memory_store_path_is_under_injected_runtime_paths_only(
    jaos_runtime_paths: RuntimePaths,
    protected_repository_state: None,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        database_path = composition.memory_store.database_path
        assert database_path.parent == jaos_runtime_paths.memory
        assert database_path.is_file()

        repository_root = _find_repository_root(Path(__file__).resolve())
        assert repository_root not in database_path.parents
    finally:
        composition.teardown()


def test_teardown_closes_and_unregisters_memory_store_exactly_once(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    store = composition.memory_store

    close_calls: list[int] = []
    original_close = store.close

    def counting_close() -> None:
        close_calls.append(1)
        original_close()

    monkeypatch.setattr(store, "close", counting_close)

    composition.teardown()

    assert close_calls == [1]
    assert store.is_closed is True
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False
    assert runtime.registry.is_registered(MEMORY_STORE_SERVICE) is False


def test_teardown_on_already_closed_store_does_not_reclose(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    store = composition.memory_store
    store.close()

    composition.teardown()

    assert store.is_closed is True
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False


def test_memory_composition_failure_closes_orphaned_store_and_leaves_no_trace(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)

    import jaos.composition.platform_composition as composition_module

    created_stores: list[SQLiteStore] = []
    original_register = composition_module.PlatformComposition._register

    def failing_register(self, name, instance):  # noqa: ANN001
        if name == MEMORY_STORE_SERVICE:
            created_stores.append(instance)
            raise RuntimeError("memory registration exploded")
        return original_register(self, name, instance)

    monkeypatch.setattr(
        composition_module.PlatformComposition, "_register", failing_register
    )

    with pytest.raises(RuntimeError, match="memory registration exploded"):
        composition.compose()

    assert len(created_stores) == 1
    assert created_stores[0].is_closed is True

    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False
    assert runtime.registry.is_registered(MEMORY_STORE_SERVICE) is False
    assert runtime.container.is_registered(TOOL_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(AI_MANAGER_SERVICE) is False
    assert runtime.container.is_registered(EXECUTIVE_CONTROLLER_SERVICE) is False


def test_memory_composition_failure_preserves_foreign_registrations(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)

    foreign_service = object()
    runtime.container.register("foreign_service", foreign_service)

    composition = PlatformComposition(runtime)

    import jaos.composition.platform_composition as composition_module

    def broken_memory_scope(*_args, **_kwargs):
        raise RuntimeError("memory scope construction exploded")

    monkeypatch.setattr(
        composition_module, "SQLiteProvider", type(
            "BrokenSQLiteProvider",
            (),
            {"from_memory_scope": staticmethod(broken_memory_scope)},
        )
    )

    with pytest.raises(RuntimeError, match="memory scope construction exploded"):
        composition.compose()

    assert runtime.container.is_registered("foreign_service") is True
    assert runtime.container.resolve("foreign_service") is foreign_service
    assert runtime.container.is_registered(MEMORY_STORE_SERVICE) is False


def test_no_legacy_memory_import_enters_canonical_composition_module():
    import jaos.composition.platform_composition as composition_module

    source = inspect.getsource(composition_module)

    assert "executive_brain" not in source
    assert "MemoryManager" not in source


def test_launcher_still_uses_a_single_composition_entrypoint():
    repository_root = _find_repository_root(Path(__file__).resolve())
    launcher_source = (repository_root / "run_jaos.py").read_text(encoding="utf-8")

    assert launcher_source.count("PlatformComposition(") == 1
    assert "MemoryPlatformComposition" not in launcher_source
    assert "IntelligencePlatformComposition" not in launcher_source


def test_each_function_scoped_composition_starts_without_a_database(
    jaos_runtime_paths: RuntimePaths,
):
    database_path = jaos_runtime_paths.memory / "memory.sqlite3"

    assert not database_path.exists()
