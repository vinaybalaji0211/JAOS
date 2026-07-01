from __future__ import annotations

from jaos_platform.platform_runtime import PlatformRuntime


class RuntimeValidator:
    """Validates the integrity of the JAOS Platform Runtime."""

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def validate(self) -> dict:
        report = {
            "container": self._validate_container(),
            "context": self._validate_context(),
            "event_bus": self._validate_event_bus(),
            "services": self._validate_services(),
        }

        report["healthy"] = all(report.values())

        return report

    def _validate_container(self) -> bool:
        return hasattr(self.runtime, "container") and (
            self.runtime.container is not None
        )

    def _validate_context(self) -> bool:
        return hasattr(self.runtime, "context") and (
            self.runtime.context is not None
        )

    def _validate_event_bus(self) -> bool:
        return hasattr(self.runtime, "events") and (
            self.runtime.events is not None
        )

    def _validate_services(self) -> bool:
        if not hasattr(self.runtime.container, "list_services"):
            return False

        services = self.runtime.container.list_services()

        required_services = {
            "service_container",
            "service_registry",
            "runtime_context",
            "event_bus",
        }

        return required_services.issubset(set(services))