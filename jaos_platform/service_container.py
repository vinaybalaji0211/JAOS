from __future__ import annotations

from jaos_platform.service_descriptor import ServiceDescriptor
from jaos_platform.service_lifetime import ServiceLifetime
from logs.logger import logger


class ServiceContainer:
    def __init__(self):
        self._services: dict[str, ServiceDescriptor] = {}

    def register(
        self,
        name: str,
        implementation,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:
        if name in self._services:
            raise ValueError(f"Service '{name}' already registered.")

        self._services[name] = ServiceDescriptor(
            name=name,
            implementation=implementation,
            lifetime=lifetime,
        )

        logger.info("Registered service: %s", name)

    def resolve(self, name: str):
        if name not in self._services:
            raise KeyError(f"Unknown service: {name}")

        return self._services[name].implementation

    def is_registered(self, name: str) -> bool:
        return name in self._services

    def list_services(self):
        return sorted(self._services.keys())