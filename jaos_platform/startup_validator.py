from __future__ import annotations

from jaos_platform.dependency_validator import DependencyValidator
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_validator import RuntimeValidator


class StartupValidator:
    """Validates that JAOS is ready to accept work."""

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def validate(self) -> dict:
        report = {
            "lifecycle_ready": self._lifecycle_ready(),
            "runtime_integrity": self._runtime_integrity(),
            "dependencies_satisfied": self._dependencies_satisfied(),
        }

        report["ready"] = all(report.values())

        return report

    def _lifecycle_ready(self) -> bool:
        return self.runtime.lifecycle_state == RuntimeLifecycleState.READY

    def _runtime_integrity(self) -> bool:
        return RuntimeValidator(self.runtime).validate()["healthy"]

    def _dependencies_satisfied(self) -> bool:
        return DependencyValidator(self.runtime).validate()["valid"]
