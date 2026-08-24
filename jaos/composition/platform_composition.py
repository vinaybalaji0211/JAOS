"""FORTRESS-05: the canonical whole-system composition root.

Composes the real AI, Tool, Executive, and Memory platforms into a
PlatformRuntime that has already reached READY, registering each as an
owned platform service so PlatformRuntime's own container/registry are the
single authoritative record of what is live. This replaces
CommandDispatcher's independent construction as the canonical production
path; CommandDispatcher keeps its own fallback construction only for
standalone/unit use.

Memory composition uses the canonical modern chain exclusively
(SQLiteProvider.from_memory_scope -> ProviderRegistry -> ProviderFactory ->
SQLiteStore) bound to this runtime's injected RuntimePaths.memory; it has no
legacy data fallback or migration. Intelligence Platform composition remains
explicitly out of scope for this slice and is not composed here.
"""

from __future__ import annotations

from jaos.ai import AIManager, ProviderManager
from jaos.ai.bootstrap import initialize_default_provider
from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.memory.providers.provider_factory import ProviderFactory
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.storage.memory_store import MemoryStore
from jaos.tools.tool_manager import ToolManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.service_metadata import ServiceMetadata

TOOL_MANAGER_SERVICE = "tool_manager_platform"
AI_MANAGER_SERVICE = "ai_manager_platform"
EXECUTIVE_CONTROLLER_SERVICE = "executive_controller_platform"
MEMORY_STORE_SERVICE = "memory_store_platform"


class CompositionError(RuntimeError):
    """Raised when platform composition is attempted or fails illegitimately."""


class CompositionTeardownError(RuntimeError):
    """Raised when one or more composed platforms failed to tear down cleanly."""


class PlatformComposition:
    """Composes AI, Tool, Executive, and Memory platforms into a started runtime."""

    def __init__(self, runtime: PlatformRuntime) -> None:
        self.runtime = runtime
        self._service_names: list[str] = []

    @property
    def tool_manager(self) -> ToolManager:
        return self.runtime.container.resolve(TOOL_MANAGER_SERVICE)

    @property
    def ai_manager(self) -> AIManager:
        return self.runtime.container.resolve(AI_MANAGER_SERVICE)

    @property
    def executive_controller(self) -> ExecutiveController:
        return self.runtime.container.resolve(EXECUTIVE_CONTROLLER_SERVICE)

    @property
    def memory_store(self) -> MemoryStore:
        return self.runtime.container.resolve(MEMORY_STORE_SERVICE)

    def compose(self) -> None:
        """Construct and register the real platforms.

        Requires the runtime to already be READY, so platform composition
        can never proceed on top of an unready runtime. Rollback-scoped: if
        a later platform fails to construct, every platform already
        registered by this call is unregistered so no live, orphaned
        platform survives a failed composition.
        """

        if self.runtime.lifecycle_state != RuntimeLifecycleState.READY:
            raise CompositionError(
                "PlatformComposition requires the runtime to be READY, got "
                f"{self.runtime.lifecycle_state.value}"
            )

        try:
            tool_manager = ToolManager()
            load_tools(tool_manager)
            self._register(TOOL_MANAGER_SERVICE, tool_manager)

            provider_manager = ProviderManager()
            ai_manager = AIManager(provider_manager)
            initialize_default_provider(provider_manager)
            self._register(AI_MANAGER_SERVICE, ai_manager)

            executive_controller = ExecutiveController(
                tool_manager,
                ai_manager=ai_manager,
            )
            self._register(EXECUTIVE_CONTROLLER_SERVICE, executive_controller)

            self._compose_memory_store()
        except Exception:
            self._rollback()
            raise

    def _compose_memory_store(self) -> None:
        """Build and register the canonical Memory store.

        Uses the modern provider chain exclusively, bound to injected
        RuntimePaths.memory: no repo-relative path, no legacy data fallback,
        no automatic migration. Registration is folded into this same
        try/except so a store that opens successfully but fails to register
        (e.g. a duplicate service name) is still closed before the failure
        propagates to compose()'s own rollback, which only unregisters names
        and never releases resources on its own.
        """

        provider = SQLiteProvider.from_memory_scope(self.runtime.runtime_paths.memory)
        registry = ProviderRegistry()
        store: MemoryStore | None = None

        try:
            registry.register(provider)
            store = ProviderFactory(registry).create_default()
            self._register(MEMORY_STORE_SERVICE, store)
        except Exception:
            if store is not None and not store.is_closed:
                store.close()
            raise

    def teardown(self) -> None:
        """Tear down composed platforms in reverse order.

        Continues past an individual platform's shutdown failure and
        aggregates every failure into one CompositionTeardownError, matching
        PlatformRuntime.stop()'s own coordinated-shutdown contract. Tool and
        Executive have no shutdown of their own today; the AI Manager's
        providers and the Memory store's SQLite connection are the only
        owned resources that require release. SQLiteStore.close() is itself
        idempotent, but the reversed self._service_names walk only ever
        visits MEMORY_STORE_SERVICE once per teardown() call regardless.
        """

        errors: list[tuple[str, Exception]] = []

        for name in reversed(self._service_names):
            if name == AI_MANAGER_SERVICE:
                try:
                    self.runtime.container.resolve(name).shutdown()
                except Exception as exc:
                    errors.append((name, exc))
            elif name == MEMORY_STORE_SERVICE:
                try:
                    store = self.runtime.container.resolve(name)
                    if not store.is_closed:
                        store.close()
                except Exception as exc:
                    errors.append((name, exc))

        self._rollback()

        if errors:
            raise CompositionTeardownError(
                "; ".join(f"{name}: {exc}" for name, exc in errors)
            )

    def _register(self, name: str, instance: object) -> None:
        self.runtime.container.register(name, instance)
        self._service_names.append(name)
        self.runtime.registry.register(
            ServiceMetadata(name=name, owner="Platform")
        )

    def _rollback(self) -> None:
        for name in reversed(self._service_names):
            if self.runtime.registry.is_registered(name):
                self.runtime.registry.unregister(name)
            if self.runtime.container.is_registered(name):
                self.runtime.container.unregister(name)

        self._service_names = []
