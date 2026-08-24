"""FORTRESS-05: the canonical whole-system composition root.

Composes the real AI, Tool, and Executive platforms into a PlatformRuntime
that has already reached READY, registering each as an owned platform
service so PlatformRuntime's own container/registry are the single
authoritative record of what is live. This replaces CommandDispatcher's
independent construction as the canonical production path; CommandDispatcher
keeps its own fallback construction only for standalone/unit use.

Memory and Intelligence Platform composition are explicitly out of scope for
this slice and are not composed here.
"""

from __future__ import annotations

from jaos.ai import AIManager, ProviderManager
from jaos.ai.bootstrap import initialize_default_provider
from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.tools.tool_manager import ToolManager
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.service_metadata import ServiceMetadata

TOOL_MANAGER_SERVICE = "tool_manager_platform"
AI_MANAGER_SERVICE = "ai_manager_platform"
EXECUTIVE_CONTROLLER_SERVICE = "executive_controller_platform"


class CompositionError(RuntimeError):
    """Raised when platform composition is attempted or fails illegitimately."""


class CompositionTeardownError(RuntimeError):
    """Raised when one or more composed platforms failed to tear down cleanly."""


class PlatformComposition:
    """Composes AI, Tool, and Executive platforms into a started runtime."""

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
        except Exception:
            self._rollback()
            raise

    def teardown(self) -> None:
        """Tear down composed platforms in reverse order.

        Continues past an individual platform's shutdown failure and
        aggregates every failure into one CompositionTeardownError, matching
        PlatformRuntime.stop()'s own coordinated-shutdown contract. Tool and
        Executive have no shutdown of their own today; only the AI Manager's
        providers require release.
        """

        errors: list[tuple[str, Exception]] = []

        for name in reversed(self._service_names):
            if name == AI_MANAGER_SERVICE:
                try:
                    self.runtime.container.resolve(name).shutdown()
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
