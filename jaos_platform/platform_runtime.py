from __future__ import annotations

import os
from pathlib import Path

from jaos_platform.event_bus import EventBus
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.lifecycle_transitions import validate_transition
from jaos_platform.runtime_context import RuntimeContext
from jaos_platform.runtime_paths import (
    DEFAULT_PROFILE_ID,
    RuntimePathConfigurationError,
    RuntimePathResolver,
    RuntimePaths,
)
from jaos_platform.service_container import ServiceContainer
from jaos_platform.service_metadata import ServiceMetadata
from jaos_platform.service_registry import ServiceRegistry
from logs.logger import configure_runtime_logging


class PartialShutdownError(RuntimeError):
    """Raised when one or more owned platform services failed to stop cleanly."""


class PlatformRuntime:
    """
    Central runtime infrastructure for JAOS.
    """

    def __init__(
        self,
        *,
        runtime_paths: RuntimePaths | None = None,
        runtime_root: os.PathLike[str] | str | None = None,
        profile_id: str = DEFAULT_PROFILE_ID,
        repository_root: os.PathLike[str] | str | None = None,
    ) -> None:

        if runtime_paths is None:
            runtime_paths = RuntimePathResolver().resolve(
                runtime_root=runtime_root,
                profile_id=profile_id,
                repository_root=repository_root,
            )
        elif not isinstance(runtime_paths, RuntimePaths):
            raise RuntimePathConfigurationError(
                "runtime_paths must be a RuntimePaths instance"
            )

        self._runtime_paths = runtime_paths
        self.container = ServiceContainer()
        self.registry = ServiceRegistry()
        self.context = RuntimeContext(runtime_paths=runtime_paths)
        self.events = EventBus()

        self._lifecycle_state = RuntimeLifecycleState.CREATED
        self._platform_service_names: list[str] = []

    @property
    def runtime_paths(self) -> RuntimePaths:
        """Return the canonical paths owned by this runtime composition."""

        return self._runtime_paths

    @property
    def lifecycle_state(self) -> RuntimeLifecycleState:
        """Return the current RuntimeLifecycleState of this runtime."""

        return self._lifecycle_state

    def configure_logging(self) -> Path:
        """Explicitly configure logging from this runtime's owned paths."""

        return configure_runtime_logging(self.runtime_paths)

    def initialize(self) -> None:
        """Advance CREATED -> INITIALIZING -> INITIALIZED."""

        self._transition(RuntimeLifecycleState.INITIALIZING)
        self._transition(RuntimeLifecycleState.INITIALIZED)

    def start(self) -> None:
        """Register and start owned platform services; advance to READY.

        On failure, undo every platform service registered by this attempt,
        transition through ROLLING_BACK to FAILED, and re-raise.
        """

        self._transition(RuntimeLifecycleState.STARTING)

        platform_services = (
            ("service_container", self.container),
            ("service_registry", self.registry),
            ("runtime_context", self.context),
            ("event_bus", self.events),
        )

        try:
            for name, implementation in platform_services:
                self.container.register(name, implementation)
                self._platform_service_names.append(name)
                self.registry.register(
                    ServiceMetadata(name=name, owner="Platform")
                )
        except Exception:
            self._teardown_platform_services()
            self._transition(RuntimeLifecycleState.ROLLING_BACK)
            self._transition(RuntimeLifecycleState.FAILED)
            raise

        self._transition(RuntimeLifecycleState.READY)

    def mark_failed(self) -> None:
        """Transition to FAILED when a required post-start validation fails."""

        self._transition(RuntimeLifecycleState.FAILED)

    def stop(self) -> None:
        """Tear down owned platform services in reverse order; advance to STOPPED.

        Individual teardown failures do not stop the unwind: every owned
        service is still given a chance to release, and any failures are
        aggregated into one PartialShutdownError raised after the attempt,
        with the runtime left truthfully FAILED rather than STOPPED.
        """

        self._transition(RuntimeLifecycleState.STOPPING)
        errors = self._teardown_platform_services()

        if errors:
            self._transition(RuntimeLifecycleState.FAILED)
            raise PartialShutdownError(
                "; ".join(f"{name}: {exc}" for name, exc in errors)
            )

        self._transition(RuntimeLifecycleState.STOPPED)

    def _transition(self, target: RuntimeLifecycleState) -> None:
        self._lifecycle_state = validate_transition(
            self._lifecycle_state, target
        )

    def _teardown_platform_services(self) -> list[tuple[str, Exception]]:
        errors: list[tuple[str, Exception]] = []

        for name in reversed(self._platform_service_names):
            try:
                if self.registry.is_registered(name):
                    self.registry.unregister(name)
            except Exception as exc:
                errors.append((f"{name}:registry", exc))

            try:
                if self.container.is_registered(name):
                    self.container.unregister(name)
            except Exception as exc:
                errors.append((f"{name}:container", exc))

        self._platform_service_names = []
        return errors
