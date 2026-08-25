"""FORTRESS-05E: executable canonical-composition closure invariants."""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import jaos.cli.command_dispatcher as dispatcher_module
import jaos.cli.shell as shell_module
import jaos.composition.platform_composition as composition_module
import run_jaos as launcher_module
from jaos.ai import AIManager
from jaos.composition import PlatformComposition
from jaos.composition.platform_composition import (
    AI_MANAGER_SERVICE,
    EXECUTIVE_CONTROLLER_SERVICE,
    INTELLIGENCE_ORCHESTRATOR_SERVICE,
    MEMORY_STORE_SERVICE,
    TOOL_MANAGER_SERVICE,
)
from jaos.executive.controller import ExecutiveController
from jaos.intelligence.conversation import ConversationOrchestrator
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos.tools.tool_approval import ToolApprovalManager
from jaos.tools.tool_audit import ToolAuditLogger
from jaos.tools.tool_manager import ToolManager
from jaos.tools.tool_permissions import ToolPermissionManager
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths
from jaos_platform.service_metadata import ServiceMetadata
from tests.tests.platform.test_canonical_import_boundary import (
    is_forbidden_runtime_module,
)

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_CANONICAL_SERVICES = (
    TOOL_MANAGER_SERVICE,
    AI_MANAGER_SERVICE,
    EXECUTIVE_CONTROLLER_SERVICE,
    MEMORY_STORE_SERVICE,
    INTELLIGENCE_ORCHESTRATOR_SERVICE,
)

_FORBIDDEN_DISPATCHER_CALLS = frozenset(
    {
        "ToolManager",
        "ProviderManager",
        "AIManager",
        "ExecutiveController",
        "load_tools",
        "initialize_default_provider",
    }
)


def _qualified_symbol(
    node: ast.expr,
    bindings: dict[str, str],
) -> str | None:
    if isinstance(node, ast.Name):
        return bindings.get(node.id, node.id)

    if isinstance(node, ast.Attribute):
        owner = _qualified_symbol(node.value, bindings)
        if owner is not None:
            return f"{owner}.{node.attr}"

    return None


def _resolved_call_targets(
    source_path: Path,
    *,
    class_name: str | None = None,
) -> list[str]:
    """Resolve direct, imported, and simply aliased call targets."""

    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    bindings: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for imported in node.names:
                bound_name = imported.asname or imported.name.split(".", 1)[0]
                bindings[bound_name] = (
                    imported.name if imported.asname else bound_name
                )
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            for imported in node.names:
                if imported.name == "*":
                    continue
                bound_name = imported.asname or imported.name
                bindings[bound_name] = f"{node.module}.{imported.name}"

    alias_assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
    ]
    for _ in range(len(alias_assignments) + 1):
        changed = False
        for node in alias_assignments:
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            if value is None:
                continue

            resolved = _qualified_symbol(value, bindings)
            if resolved is None:
                continue

            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                if resolved == target.id or resolved.startswith(f"{target.id}."):
                    continue
                if bindings.get(target.id) != resolved:
                    bindings[target.id] = resolved
                    changed = True
        if not changed:
            break

    scope: ast.AST = tree
    if class_name is not None:
        matching_classes = [
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == class_name
        ]
        assert len(matching_classes) == 1, class_name
        scope = matching_classes[0]

    targets: list[str] = []
    for node in ast.walk(scope):
        if not isinstance(node, ast.Call):
            continue
        resolved = _qualified_symbol(node.func, bindings)
        if resolved is not None:
            targets.append(resolved)

    return targets


def _started_runtime(runtime_paths: RuntimePaths) -> PlatformRuntime:
    runtime = PlatformRuntime(runtime_paths=runtime_paths)
    runtime.initialize()
    runtime.start()
    return runtime


def _canonical_instances(runtime: PlatformRuntime) -> dict[str, object]:
    return {name: runtime.container.resolve(name) for name in _CANONICAL_SERVICES}


def test_exactly_five_canonical_authorities_share_one_live_object_graph(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        instances = _canonical_instances(runtime)

        assert set(instances) == set(_CANONICAL_SERVICES)
        assert len({id(instance) for instance in instances.values()}) == 5
        assert composition.tool_manager is instances[TOOL_MANAGER_SERVICE]
        assert composition.ai_manager is instances[AI_MANAGER_SERVICE]
        assert (
            composition.executive_controller is instances[EXECUTIVE_CONTROLLER_SERVICE]
        )
        assert composition.memory_store is instances[MEMORY_STORE_SERVICE]
        assert (
            composition.intelligence_orchestrator
            is instances[INTELLIGENCE_ORCHESTRATOR_SERVICE]
        )

        expected_types = (
            ToolManager,
            AIManager,
            ExecutiveController,
            SQLiteStore,
            ConversationOrchestrator,
        )
        for expected_type in expected_types:
            matches = [
                runtime.container.resolve(name)
                for name in runtime.container.list_services()
                if isinstance(runtime.container.resolve(name), expected_type)
            ]
            assert len(matches) == 1, expected_type.__name__

        executive = composition.executive_controller
        assert executive.execution_coordinator.tool_manager is composition.tool_manager
        assert (
            executive.ai_reasoning_service.gateway._ai_manager is composition.ai_manager
        )
        assert (
            composition.intelligence_orchestrator._ai_manager is composition.ai_manager
        )
    finally:
        composition.teardown()


def test_canonical_tool_authority_reaches_existing_control_interfaces(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        tool_manager = composition.tool_manager
        engine = tool_manager._execution_engine

        assert isinstance(tool_manager._permissions, ToolPermissionManager)
        assert isinstance(tool_manager._approval_manager, ToolApprovalManager)
        assert isinstance(tool_manager._audit_logger, ToolAuditLogger)
        assert engine._permissions is tool_manager._permissions
        assert engine._approval_manager is tool_manager._approval_manager
        assert engine._audit_logger is tool_manager._audit_logger
    finally:
        composition.teardown()


def test_load_tools_failure_preserves_original_and_leaves_no_owned_service(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    failure = RuntimeError("tool loading exploded")

    def fail_load_tools(_tool_manager: ToolManager) -> None:
        raise failure

    monkeypatch.setattr(composition_module, "load_tools", fail_load_tools)

    composition = PlatformComposition(runtime)
    with pytest.raises(RuntimeError) as error:
        composition.compose()

    assert error.value is failure
    for name in _CANONICAL_SERVICES:
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False


def test_default_provider_initialization_failure_shuts_down_partial_ai(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    failure = RuntimeError("default provider initialization exploded")
    captured: dict[str, object] = {}
    original_initialize = composition_module.initialize_default_provider

    def initialize_then_fail(provider_manager: object) -> None:
        original_initialize(provider_manager)
        captured["provider"] = provider_manager.get_provider("mock")
        raise failure

    monkeypatch.setattr(
        composition_module,
        "initialize_default_provider",
        initialize_then_fail,
    )

    composition = PlatformComposition(runtime)
    with pytest.raises(RuntimeError) as error:
        composition.compose()

    assert error.value is failure
    assert captured["provider"]._initialized is False
    for name in _CANONICAL_SERVICES:
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False


def test_ai_registration_failure_cleans_provider_without_masking_original(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    foreign_service = object()
    foreign_metadata = ServiceMetadata(
        name="foreign_service",
        owner="Foreign",
    )
    runtime.container.register("foreign_service", foreign_service)
    runtime.registry.register(foreign_metadata)

    registration_error = RuntimeError("AI registration exploded")
    cleanup_error = RuntimeError("AI cleanup reporting exploded")
    captured: dict[str, object] = {}
    shutdown_calls = 0
    original_register = composition_module.PlatformComposition._register
    original_shutdown = composition_module.AIManager.shutdown

    def failing_register(
        self: PlatformComposition,
        name: str,
        instance: object,
        **kwargs: object,
    ) -> None:
        if name == AI_MANAGER_SERVICE:
            captured["manager"] = instance
            raise registration_error
        original_register(self, name, instance, **kwargs)

    def shutdown_then_report_failure(self: AIManager) -> None:
        nonlocal shutdown_calls
        shutdown_calls += 1
        original_shutdown(self)
        if shutdown_calls == 1:
            raise cleanup_error

    monkeypatch.setattr(
        composition_module.PlatformComposition,
        "_register",
        failing_register,
    )
    monkeypatch.setattr(
        composition_module.AIManager,
        "shutdown",
        shutdown_then_report_failure,
    )

    composition = PlatformComposition(runtime)
    with pytest.raises(RuntimeError) as error:
        composition.compose()

    manager = captured["manager"]
    provider = manager.get_provider_manager().get_provider("mock")
    assert error.value is registration_error
    assert any(
        "AI cleanup reporting exploded" in note
        for note in getattr(error.value, "__notes__", ())
    )
    assert provider._initialized is False
    assert manager._shutdown_complete is True
    assert composition._pending_ai_manager is manager
    assert runtime.container.resolve("foreign_service") is foreign_service
    assert runtime.registry.get("foreign_service") is foreign_metadata
    for name in _CANONICAL_SERVICES:
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False

    composition.teardown()

    assert shutdown_calls == 2
    assert composition._pending_ai_manager is None

    composition.teardown()
    assert shutdown_calls == 2


def test_ast_call_resolver_follows_import_and_assignment_aliases(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "aliased_dispatcher.py"
    source_path.write_text(
        """from jaos.tools.tool_manager import ToolManager as TM
import jaos.ai as platform_ai
from jaos.ai.bootstrap import initialize_default_provider as init
from jaos.bootstrap.tool_loader import load_tools as load
from jaos.executive.controller import ExecutiveController as EC

build_executive = EC


class CommandDispatcher:
    def __init__(self):
        build_tools = TM
        build_tools()
        platform_ai.ProviderManager()
        platform_ai.AIManager()
        build_executive()
        load(None)
        init(None)
""",
        encoding="utf-8",
    )

    terminals = {
        target.rsplit(".", 1)[-1]
        for target in _resolved_call_targets(
            source_path,
            class_name="CommandDispatcher",
        )
    }

    assert terminals == _FORBIDDEN_DISPATCHER_CALLS


def test_command_dispatcher_is_not_a_hidden_composition_root() -> None:
    call_targets = _resolved_call_targets(
        Path(dispatcher_module.__file__),
        class_name="CommandDispatcher",
    )
    forbidden_targets = {
        target
        for target in call_targets
        if target.rsplit(".", 1)[-1] in _FORBIDDEN_DISPATCHER_CALLS
    }

    assert forbidden_targets == set()


def test_shell_does_not_construct_a_command_dispatcher() -> None:
    call_targets = _resolved_call_targets(
        Path(shell_module.__file__),
        class_name="JAOSShell",
    )

    assert all(
        target.rsplit(".", 1)[-1] != "CommandDispatcher"
        for target in call_targets
    )


def test_cli_constructors_require_explicit_valid_dependencies_before_helpers(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    helper_calls: list[str] = []

    def forbidden_helper(*_args: object, **_kwargs: object) -> object:
        helper_calls.append("called")
        raise AssertionError("dispatcher helper reached before validation")

    monkeypatch.setattr(
        dispatcher_module.ProviderProfileRegistry,
        "build_default",
        forbidden_helper,
    )
    monkeypatch.setattr(
        dispatcher_module,
        "ProviderStatusService",
        forbidden_helper,
    )

    try:
        with pytest.raises(TypeError):
            dispatcher_module.CommandDispatcher()
        with pytest.raises(TypeError):
            dispatcher_module.CommandDispatcher(composition.tool_manager)
        with pytest.raises(TypeError):
            dispatcher_module.CommandDispatcher(
                composition.tool_manager,
                ai_manager=composition.ai_manager,
            )

        valid_dependencies = {
            "tool_manager": composition.tool_manager,
            "ai_manager": composition.ai_manager,
            "executive": composition.executive_controller,
        }
        for dependency_name in valid_dependencies:
            invalid_dependencies = dict(valid_dependencies)
            invalid_dependencies[dependency_name] = None
            with pytest.raises(TypeError):
                dispatcher_module.CommandDispatcher(**invalid_dependencies)

        with pytest.raises(TypeError):
            shell_module.JAOSShell()
        with pytest.raises(TypeError):
            shell_module.JAOSShell(None)
    finally:
        composition.teardown()

    assert helper_calls == []


def test_canonical_launcher_injects_exact_composition_identities(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    observed: dict[str, object] = {}
    runtime = PlatformRuntime(runtime_paths=jaos_runtime_paths)

    def inspect_real_shell(self: shell_module.JAOSShell) -> None:
        dispatcher = self.dispatcher
        instances = _canonical_instances(runtime)
        observed["real_shell"] = isinstance(self, shell_module.JAOSShell)
        observed["tool_identity"] = (
            dispatcher.tool_manager is instances[TOOL_MANAGER_SERVICE]
        )
        observed["ai_identity"] = (
            dispatcher.ai_manager is instances[AI_MANAGER_SERVICE]
        )
        observed["executive_identity"] = (
            dispatcher.executive is instances[EXECUTIVE_CONTROLLER_SERVICE]
        )
        observed["has_shutdown"] = hasattr(dispatcher, "shutdown")
        observed["has_owns_ai_manager"] = hasattr(
            dispatcher,
            "_owns_ai_manager",
        )
        observed["ai_manager"] = dispatcher.ai_manager
        observed["canonical_instance_count"] = len(
            {id(instance) for instance in instances.values()}
        )

    monkeypatch.setattr(shell_module.JAOSShell, "run", inspect_real_shell)

    exit_code = launcher_module.JAOSApplication(runtime=runtime).run()
    capsys.readouterr()

    assert exit_code == 0
    assert observed["real_shell"] is True
    assert observed["tool_identity"] is True
    assert observed["ai_identity"] is True
    assert observed["executive_identity"] is True
    assert observed["has_shutdown"] is False
    assert observed["has_owns_ai_manager"] is False
    assert observed["canonical_instance_count"] == 5
    assert observed["ai_manager"]._shutdown_complete is True
    assert runtime.container.list_services() == []


def test_clean_launcher_import_does_not_load_deferred_capability_modules() -> None:
    script = "import json, sys; import run_jaos; print(json.dumps(sorted(sys.modules)))"
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=_REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    loaded_modules = json.loads(result.stdout.strip().splitlines()[-1])

    assert "jaos.intelligence.conversation.conversation_orchestrator" in (
        loaded_modules
    )
    assert "jaos.intelligence.prompt.prompt_composer" in loaded_modules
    assert not any(
        is_forbidden_runtime_module(module) for module in loaded_modules
    )


def test_lazy_submodule_compatibility_does_not_load_deferred_capabilities() -> None:
    script = (
        "import json, sys; import jaos.intelligence as intelligence; "
        "assert intelligence.models.__name__ == 'jaos.intelligence.models'; "
        "assert intelligence.context.__name__ == 'jaos.intelligence.context'; "
        "assert intelligence.exceptions.__name__ == "
        "'jaos.intelligence.exceptions'; "
        "assert intelligence.interfaces.__name__ == "
        "'jaos.intelligence.interfaces'; "
        "assert intelligence.prompt.__name__ == 'jaos.intelligence.prompt'; "
        "print(json.dumps(sorted(sys.modules)))"
    )
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=_REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    loaded_modules = json.loads(result.stdout.strip().splitlines()[-1])

    assert "jaos.intelligence.models" in loaded_modules
    assert "jaos.intelligence.context" in loaded_modules
    assert "jaos.intelligence.exceptions" in loaded_modules
    assert "jaos.intelligence.interfaces" in loaded_modules
    assert "jaos.intelligence.prompt" in loaded_modules
    assert not any(
        is_forbidden_runtime_module(module) for module in loaded_modules
    )


def test_forbidden_lazy_facade_access_is_detectable_by_runtime_guard() -> None:
    script = (
        "import json, sys; import jaos.intelligence as intelligence; "
        "intelligence.MemoryContextSource; "
        "print(json.dumps(sorted(sys.modules)))"
    )
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=_REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    loaded_modules = json.loads(result.stdout.strip().splitlines()[-1])
    detected = [
        module
        for module in loaded_modules
        if is_forbidden_runtime_module(module)
    ]

    assert "jaos.intelligence.context.memory_context_source" in detected


def test_late_composition_failure_rolls_back_the_whole_owned_graph(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    foreign_service = object()
    foreign_metadata = ServiceMetadata(name="foreign_service", owner="Foreign")
    runtime.container.register("foreign_service", foreign_service)
    runtime.registry.register(foreign_metadata)

    created: dict[str, object] = {}
    shutdown_events: list[str] = []
    failure = RuntimeError("canonical graph registration exploded")
    original_register = composition_module.PlatformComposition._register
    original_orchestrator_shutdown = (
        composition_module.ConversationOrchestrator.shutdown
    )
    original_prompt_shutdown = composition_module.IntelligencePromptComposer.shutdown
    original_store_close = SQLiteStore.close
    original_ai_shutdown = composition_module.AIManager.shutdown

    def recording_orchestrator_shutdown(self: object) -> None:
        shutdown_events.append("intelligence_orchestrator")
        original_orchestrator_shutdown(self)

    def recording_prompt_shutdown(self: object) -> None:
        shutdown_events.append("intelligence_prompt_composer")
        original_prompt_shutdown(self)

    def recording_store_close(self: SQLiteStore) -> None:
        shutdown_events.append("memory_store")
        original_store_close(self)

    def recording_ai_shutdown(self: AIManager) -> None:
        shutdown_events.append("ai_manager")
        original_ai_shutdown(self)

    def failing_register(
        self: PlatformComposition,
        name: str,
        instance: object,
        **kwargs: object,
    ) -> None:
        created[name] = instance
        if name == INTELLIGENCE_ORCHESTRATOR_SERVICE:
            raise failure
        original_register(self, name, instance, **kwargs)

    monkeypatch.setattr(
        composition_module.ConversationOrchestrator,
        "shutdown",
        recording_orchestrator_shutdown,
    )
    monkeypatch.setattr(
        composition_module.IntelligencePromptComposer,
        "shutdown",
        recording_prompt_shutdown,
    )
    monkeypatch.setattr(SQLiteStore, "close", recording_store_close)
    monkeypatch.setattr(
        composition_module.AIManager,
        "shutdown",
        recording_ai_shutdown,
    )
    monkeypatch.setattr(
        composition_module.PlatformComposition,
        "_register",
        failing_register,
    )

    composition = PlatformComposition(runtime)
    with pytest.raises(RuntimeError) as error:
        composition.compose()

    assert error.value is failure
    assert set(created) == set(_CANONICAL_SERVICES)
    assert shutdown_events == [
        "intelligence_orchestrator",
        "intelligence_prompt_composer",
        "memory_store",
        "ai_manager",
    ]
    assert created[MEMORY_STORE_SERVICE].is_closed is True
    assert created[AI_MANAGER_SERVICE]._shutdown_complete is True
    assert created[INTELLIGENCE_ORCHESTRATOR_SERVICE].is_ready is False

    for name in _CANONICAL_SERVICES:
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False

    assert runtime.container.resolve("foreign_service") is foreign_service
    assert runtime.registry.get("foreign_service") is foreign_metadata

    composition.teardown()
    assert shutdown_events == [
        "intelligence_orchestrator",
        "intelligence_prompt_composer",
        "memory_store",
        "ai_manager",
    ]


def test_teardown_is_reverse_order_idempotent_and_removes_all_services(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    orchestrator = composition.intelligence_orchestrator
    prompt_composer = orchestrator._prompt_composer
    store = composition.memory_store
    ai_manager = composition.ai_manager
    events: list[str] = []

    original_orchestrator_shutdown = orchestrator.shutdown
    original_prompt_shutdown = prompt_composer.shutdown
    original_store_close = store.close
    original_ai_shutdown = ai_manager.shutdown

    def shutdown_orchestrator() -> None:
        events.append("intelligence_orchestrator")
        original_orchestrator_shutdown()

    def shutdown_prompt() -> None:
        events.append("intelligence_prompt_composer")
        original_prompt_shutdown()

    def close_store() -> None:
        events.append("memory_store")
        original_store_close()

    def shutdown_ai() -> None:
        events.append("ai_manager")
        original_ai_shutdown()

    monkeypatch.setattr(orchestrator, "shutdown", shutdown_orchestrator)
    monkeypatch.setattr(prompt_composer, "shutdown", shutdown_prompt)
    monkeypatch.setattr(store, "close", close_store)
    monkeypatch.setattr(ai_manager, "shutdown", shutdown_ai)

    composition.teardown()
    composition.teardown()

    assert events == [
        "intelligence_orchestrator",
        "intelligence_prompt_composer",
        "memory_store",
        "ai_manager",
    ]
    assert store.is_closed is True
    assert ai_manager._shutdown_complete is True
    for name in _CANONICAL_SERVICES:
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False


def test_run_jaos_is_the_only_production_platform_composition_root() -> None:
    production_sources = [
        _REPOSITORY_ROOT / "run_jaos.py",
        *_REPOSITORY_ROOT.joinpath("jaos").rglob("*.py"),
        *_REPOSITORY_ROOT.joinpath("jaos_platform").rglob("*.py"),
    ]
    composition_calls: list[Path] = []

    for source_path in production_sources:
        for target in _resolved_call_targets(source_path):
            if target.rsplit(".", 1)[-1] == "PlatformComposition":
                composition_calls.append(source_path)

    assert composition_calls == [_REPOSITORY_ROOT / "run_jaos.py"]
