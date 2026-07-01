from __future__ import annotations

from jaos_platform.platform_runtime import PlatformRuntime


class StartupValidator:
    """Validates that JAOS is ready to accept work."""

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def validate(self) -> dict:
        report = {
            "boot_status": self._boot_ready(),
            "configuration": self._configuration_ready(),
            "executive_brain": self._executive_ready(),
            "startup_services": self._startup_services_ready(),
        }

        report["ready"] = all(report.values())

        return report

    def _boot_ready(self) -> bool:
        return self.runtime.context.get("boot_status") == "READY"

    def _configuration_ready(self) -> bool:
        return (
            self.runtime.context.get("config_manager_status")
            == "READY"
        )

    def _executive_ready(self) -> bool:
        return (
            self.runtime.context.get("executive_brain_status")
            == "READY"
        )

    def _startup_services_ready(self) -> bool:
        return (
            self.runtime.context.get("startup_manager_status")
            == "READY"
        )