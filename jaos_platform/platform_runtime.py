from __future__ import annotations

from jaos_platform.event_bus import EventBus
from jaos_platform.runtime_context import RuntimeContext
from jaos_platform.service_container import ServiceContainer
from jaos_platform.service_metadata import ServiceMetadata
from jaos_platform.service_registry import ServiceRegistry


class PlatformRuntime:
    """
    Central runtime infrastructure for JAOS.
    """

    def __init__(self) -> None:

        self.container = ServiceContainer()
        self.registry = ServiceRegistry()
        self.context = RuntimeContext()
        self.events = EventBus()

        self._register_platform_services()

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