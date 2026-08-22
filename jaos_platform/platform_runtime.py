from __future__ import annotations

import os
from pathlib import Path

from jaos_platform.event_bus import EventBus
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

        self._register_platform_services()

    @property
    def runtime_paths(self) -> RuntimePaths:
        """Return the canonical paths owned by this runtime composition."""

        return self._runtime_paths

    def configure_logging(self) -> Path:
        """Explicitly configure logging from this runtime's owned paths."""

        return configure_runtime_logging(self.runtime_paths)

    def _register_platform_services(self):

        self.container.register("service_container", self.container)
        self.container.register("service_registry", self.registry)
        self.container.register("runtime_context", self.context)
        self.container.register("event_bus", self.events)

        self.registry.register(ServiceMetadata(
            name="service_container",
            owner="Platform",
        ))

        self.registry.register(ServiceMetadata(
            name="service_registry",
            owner="Platform",
        ))

        self.registry.register(ServiceMetadata(
            name="runtime_context",
            owner="Platform",
        ))

        self.registry.register(ServiceMetadata(
            name="event_bus",
            owner="Platform",
        ))
