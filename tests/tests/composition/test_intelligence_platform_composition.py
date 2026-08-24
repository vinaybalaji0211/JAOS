"""FORTRESS-05D: canonical Conversation Intelligence composition."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from jaos.composition import CompositionError, PlatformComposition
from jaos.composition.platform_composition import (
    AI_MANAGER_SERVICE,
    EXECUTIVE_CONTROLLER_SERVICE,
    INTELLIGENCE_ORCHESTRATOR_SERVICE,
    MEMORY_STORE_SERVICE,
    TOOL_MANAGER_SERVICE,
)
from jaos.intelligence.conversation import (
    ConversationOrchestrator,
    ConversationPolicy,
    ConversationPolicyRegistry,
    ConversationReferenceResolver,
    ConversationSessionManager,
    InMemoryConversationSessionStore,
)
from jaos.intelligence.prompt import (
    IntelligencePromptComposer,
    IntelligencePromptTemplate,
    PromptTemplateRegistry,
)
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_paths import RuntimePaths
from jaos_platform.service_metadata import ServiceMetadata

_SYSTEM_INSTRUCTION = (
    "You are the conversational intelligence component of JAOS. "
    "Respond using the supplied conversation context, policy, and resolved "
    "references. Do not claim that tools, actions, approvals, or external "
    "operations occurred unless their results are explicitly provided."
)
_TASK_INSTRUCTION = (
    "Produce a helpful response to the user's current message. "
    "Preserve conversational continuity and respect the supplied context and "
    "policy."
)


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


def test_canonical_orchestrator_registration_identity_and_object_graph(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        orchestrator = composition.intelligence_orchestrator

        assert isinstance(orchestrator, ConversationOrchestrator)
        assert (
            runtime.container.resolve(INTELLIGENCE_ORCHESTRATOR_SERVICE)
            is orchestrator
        )

        composed_orchestrators = [
            runtime.container.resolve(name)
            for name in runtime.container.list_services()
            if isinstance(
                runtime.container.resolve(name),
                ConversationOrchestrator,
            )
        ]
        assert composed_orchestrators == [orchestrator]

        metadata = runtime.registry.get(INTELLIGENCE_ORCHESTRATOR_SERVICE)
        assert metadata.name == INTELLIGENCE_ORCHESTRATOR_SERVICE
        assert metadata.owner == "Intelligence"
        assert [
            name
            for name in runtime.registry.list()
            if runtime.registry.get(name).owner == "Intelligence"
        ] == [INTELLIGENCE_ORCHESTRATOR_SERVICE]

        assert isinstance(
            orchestrator._session_manager,
            ConversationSessionManager,
        )
        assert isinstance(
            orchestrator._session_manager._session_store,
            InMemoryConversationSessionStore,
        )
        assert isinstance(
            orchestrator._policy_registry,
            ConversationPolicyRegistry,
        )
        assert (
            orchestrator._session_manager._policy_registry
            is orchestrator._policy_registry
        )
        assert isinstance(
            orchestrator._reference_resolver,
            ConversationReferenceResolver,
        )
        assert isinstance(
            orchestrator._prompt_composer,
            IntelligencePromptComposer,
        )
        assert orchestrator._ai_manager is composition.ai_manager
        assert orchestrator._template_id == "conversation"
        assert orchestrator._template_version is None
        assert orchestrator._prompt_composer.is_ready is True
        assert orchestrator.is_ready is True

        assert not hasattr(composition, "prompt_composer")
        assert not hasattr(composition, "conversation_session_manager")
    finally:
        composition.teardown()


def test_approved_default_policy_and_conversation_template_are_registered(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        orchestrator = composition.intelligence_orchestrator
        policy_registry = orchestrator._policy_registry
        template_registry = orchestrator._prompt_composer._template_registry

        assert len(policy_registry) == 1
        assert policy_registry.default_policy_name == "default"
        assert policy_registry.resolve_policy() == ConversationPolicy(
            policy_name="default"
        )

        assert isinstance(template_registry, PromptTemplateRegistry)
        assert len(template_registry) == 1
        assert template_registry.resolve_template(
            "conversation"
        ) == IntelligencePromptTemplate(
            template_id="conversation",
            version="1.0",
            system_instruction=_SYSTEM_INSTRUCTION,
            task_instruction=_TASK_INSTRUCTION,
        )
    finally:
        composition.teardown()


def test_prompt_composer_initializes_before_orchestrator(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)

    import jaos.composition.platform_composition as composition_module

    events: list[tuple[str, bool, bool | None]] = []
    original_composer_initialize = (
        composition_module.IntelligencePromptComposer.initialize
    )
    original_orchestrator_initialize = (
        composition_module.ConversationOrchestrator.initialize
    )

    def recording_composer_initialize(self):  # noqa: ANN001
        events.append(("prompt_composer", self.is_ready, None))
        original_composer_initialize(self)

    def recording_orchestrator_initialize(self):  # noqa: ANN001
        events.append(
            (
                "conversation_orchestrator",
                self.is_ready,
                self._prompt_composer.is_ready,
            )
        )
        original_orchestrator_initialize(self)

    monkeypatch.setattr(
        composition_module.IntelligencePromptComposer,
        "initialize",
        recording_composer_initialize,
    )
    monkeypatch.setattr(
        composition_module.ConversationOrchestrator,
        "initialize",
        recording_orchestrator_initialize,
    )

    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        assert events == [
            ("prompt_composer", False, None),
            ("conversation_orchestrator", False, True),
        ]
        assert composition.intelligence_orchestrator.is_ready is True
        assert not inspect.iscoroutinefunction(
            composition_module.IntelligencePromptComposer.initialize
        )
        assert not inspect.iscoroutinefunction(
            composition_module.ConversationOrchestrator.initialize
        )
    finally:
        composition.teardown()


def test_teardown_shuts_down_intelligence_in_order_without_double_shutdown(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    orchestrator = composition.intelligence_orchestrator
    prompt_composer = orchestrator._prompt_composer

    events: list[str] = []
    original_orchestrator_shutdown = orchestrator.shutdown
    original_composer_shutdown = prompt_composer.shutdown

    def recording_orchestrator_shutdown() -> None:
        events.append("conversation_orchestrator")
        original_orchestrator_shutdown()

    def recording_composer_shutdown() -> None:
        events.append("prompt_composer")
        original_composer_shutdown()

    monkeypatch.setattr(
        orchestrator,
        "shutdown",
        recording_orchestrator_shutdown,
    )
    monkeypatch.setattr(
        prompt_composer,
        "shutdown",
        recording_composer_shutdown,
    )

    composition.teardown()
    composition.teardown()

    assert events == ["conversation_orchestrator", "prompt_composer"]
    assert orchestrator.is_ready is False
    assert prompt_composer.is_ready is False
    assert runtime.container.is_registered(
        INTELLIGENCE_ORCHESTRATOR_SERVICE
    ) is False
    assert runtime.registry.is_registered(
        INTELLIGENCE_ORCHESTRATOR_SERVICE
    ) is False


def test_intelligence_registration_failure_cleans_lifecycle_and_propagates(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)

    import jaos.composition.platform_composition as composition_module

    created: dict[str, object] = {}
    shutdown_events: list[str] = []
    original_register = composition_module.PlatformComposition._register
    original_orchestrator_shutdown = (
        composition_module.ConversationOrchestrator.shutdown
    )
    original_composer_shutdown = (
        composition_module.IntelligencePromptComposer.shutdown
    )

    def recording_orchestrator_shutdown(self):  # noqa: ANN001
        shutdown_events.append("conversation_orchestrator")
        original_orchestrator_shutdown(self)

    def recording_composer_shutdown(self):  # noqa: ANN001
        shutdown_events.append("prompt_composer")
        original_composer_shutdown(self)

    def failing_register(self, name, instance, **kwargs):  # noqa: ANN001
        created[name] = instance
        if name == INTELLIGENCE_ORCHESTRATOR_SERVICE:
            raise RuntimeError("intelligence registration exploded")
        return original_register(self, name, instance, **kwargs)

    monkeypatch.setattr(
        composition_module.ConversationOrchestrator,
        "shutdown",
        recording_orchestrator_shutdown,
    )
    monkeypatch.setattr(
        composition_module.IntelligencePromptComposer,
        "shutdown",
        recording_composer_shutdown,
    )
    monkeypatch.setattr(
        composition_module.PlatformComposition,
        "_register",
        failing_register,
    )

    composition = PlatformComposition(runtime)

    with pytest.raises(
        RuntimeError,
        match="intelligence registration exploded",
    ):
        composition.compose()

    orchestrator = created[INTELLIGENCE_ORCHESTRATOR_SERVICE]
    prompt_composer = orchestrator._prompt_composer

    assert shutdown_events == [
        "conversation_orchestrator",
        "prompt_composer",
    ]
    assert orchestrator.is_ready is False
    assert prompt_composer.is_ready is False
    assert composition._intelligence_orchestrator is None
    assert composition._prompt_composer is None
    assert runtime.container.is_registered(
        INTELLIGENCE_ORCHESTRATOR_SERVICE
    ) is False
    assert runtime.registry.is_registered(
        INTELLIGENCE_ORCHESTRATOR_SERVICE
    ) is False

    for name in (
        TOOL_MANAGER_SERVICE,
        AI_MANAGER_SERVICE,
        EXECUTIVE_CONTROLLER_SERVICE,
        MEMORY_STORE_SERVICE,
    ):
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False

    memory_store = created[MEMORY_STORE_SERVICE]
    assert memory_store.is_closed is True


def test_failed_attempt_preserves_conflicting_foreign_registrations(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    foreign_service = object()
    foreign_metadata = ServiceMetadata(
        name=INTELLIGENCE_ORCHESTRATOR_SERVICE,
        owner="Foreign",
    )
    runtime.container.register("foreign_service", foreign_service)
    runtime.registry.register(
        ServiceMetadata(name="foreign_service", owner="Foreign")
    )
    runtime.registry.register(foreign_metadata)

    composition = PlatformComposition(runtime)

    with pytest.raises(ValueError, match="already exists"):
        composition.compose()

    assert runtime.container.resolve("foreign_service") is foreign_service
    assert runtime.registry.get("foreign_service").owner == "Foreign"
    assert (
        runtime.registry.get(INTELLIGENCE_ORCHESTRATOR_SERVICE)
        is foreign_metadata
    )
    assert runtime.container.is_registered(
        INTELLIGENCE_ORCHESTRATOR_SERVICE
    ) is False

    for name in (
        TOOL_MANAGER_SERVICE,
        AI_MANAGER_SERVICE,
        EXECUTIVE_CONTROLLER_SERVICE,
        MEMORY_STORE_SERVICE,
    ):
        assert runtime.container.is_registered(name) is False
        assert runtime.registry.is_registered(name) is False


def test_intelligence_composition_preserves_existing_platform_identities(
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
):
    runtime = _started_runtime(jaos_runtime_paths)

    import jaos.composition.platform_composition as composition_module

    observed: dict[str, tuple[object, object, object, object]] = {}
    original_compose_intelligence = (
        composition_module.PlatformComposition
        ._compose_intelligence_orchestrator
    )

    def observing_compose_intelligence(self, ai_manager):  # noqa: ANN001
        observed["before"] = (
            self.tool_manager,
            self.ai_manager,
            self.executive_controller,
            self.memory_store,
        )
        assert ai_manager is self.ai_manager
        original_compose_intelligence(self, ai_manager)
        observed["after"] = (
            self.tool_manager,
            self.ai_manager,
            self.executive_controller,
            self.memory_store,
        )

    monkeypatch.setattr(
        composition_module.PlatformComposition,
        "_compose_intelligence_orchestrator",
        observing_compose_intelligence,
    )

    composition = PlatformComposition(runtime)
    composition.compose()

    try:
        assert observed["after"] == observed["before"]
        assert composition.intelligence_orchestrator._ai_manager is observed[
            "before"
        ][1]
    finally:
        composition.teardown()


def test_repeated_compose_keeps_one_ready_canonical_orchestrator(
    jaos_runtime_paths: RuntimePaths,
):
    runtime = _started_runtime(jaos_runtime_paths)
    composition = PlatformComposition(runtime)
    composition.compose()
    orchestrator = composition.intelligence_orchestrator

    try:
        with pytest.raises(CompositionError, match="already composed"):
            composition.compose()

        assert composition.intelligence_orchestrator is orchestrator
        assert orchestrator.is_ready is True
        assert runtime.container.list_services().count(
            INTELLIGENCE_ORCHESTRATOR_SERVICE
        ) == 1
    finally:
        composition.teardown()


def test_composition_import_boundary_excludes_ms0025e_and_memory_context():
    import jaos.composition.platform_composition as composition_module

    source = inspect.getsource(composition_module)
    tree = ast.parse(source)
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imported_modules.update(
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    )

    assert not any(
        module.startswith(
            (
                "jaos.intelligence.planning",
                "jaos.intelligence.reasoning",
                "jaos.intelligence.agent",
            )
        )
        for module in imported_modules
    )
    assert "AgentOrchestrator" not in source
    assert "ExecutionProposalBuilder" not in source
    assert "MemoryContextSource" not in source
    assert "MemorySearchEngine" not in source
    assert "executive_brain" not in source


def test_launcher_keeps_single_platform_composition_root():
    repository_root = _find_repository_root(Path(__file__).resolve())
    launcher_source = (repository_root / "run_jaos.py").read_text(
        encoding="utf-8"
    )

    assert launcher_source.count("PlatformComposition(") == 1
    assert "IntelligencePlatformComposition" not in launcher_source
