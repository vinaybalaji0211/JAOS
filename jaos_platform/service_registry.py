from __future__ import annotations

from jaos_platform.service_metadata import ServiceMetadata
from logs.logger import logger


class ServiceRegistry:
    """Central registry for JAOS service metadata."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceMetadata] = {}

    def register(self, metadata: ServiceMetadata) -> None:
        if metadata.name in self._services:
            raise ValueError(f"Service '{metadata.name}' already exists.")

        self._services[metadata.name] = metadata
        logger.info("Registered service metadata: %s", metadata.name)

    def get(self, name: str) -> ServiceMetadata:
        if name not in self._services:
            raise KeyError(f"Unknown service: {name}")

        return self._services[name]

    def list(self) -> list[str]:
        return sorted(self._services.keys())

    def update_status(self, name: str, status: str) -> None:
        self.get(name).status = status

    def is_registered(self, name: str) -> bool:
        return name in self._services

    def unregister(self, name: str) -> None:
        if name not in self._services:
            raise KeyError(f"Unknown service: {name}")

        del self._services[name]

        logger.info("Unregistered service metadata: %s", name)