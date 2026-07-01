from __future__ import annotations

from jaos_platform.platform_runtime import PlatformRuntime


class DependencyValidator:
    """Validates runtime service dependencies."""

    REQUIRED_SERVICES = {
        "service_container",
        "service_registry",
        "runtime_context",
        "event_bus",
    }

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def validate(self) -> dict:
        services = set(
            self.runtime.container.list_services()
        )

        missing = sorted(
            self.REQUIRED_SERVICES - services
        )

        report = {
            "valid": len(missing) == 0,
            "registered_services": len(services),
            "missing_services": missing,
        }

        return report