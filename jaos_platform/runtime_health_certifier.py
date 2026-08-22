from jaos_platform.health_status import HealthStatus
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime


class RuntimeHealthCertifier:
    """Certifies the health of the JAOS runtime."""

    _SERVICE_CHECKS = {
        "service_container": lambda runtime: runtime.container is not None,
        "service_registry": lambda runtime: runtime.registry is not None,
        "runtime_context": lambda runtime: runtime.context is not None,
        "event_bus": lambda runtime: runtime.events is not None,
    }

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def certify(self) -> dict:
        services = self.runtime.container.list_services()

        report: dict[str, HealthStatus] = {}

        for service in services:
            report[service] = self._check_service(service)

        report["overall"] = self._overall(report)

        return report

    def _check_service(self, service: str) -> HealthStatus:
        check = self._SERVICE_CHECKS.get(service)

        if check is None:
            return HealthStatus.UNKNOWN

        try:
            return HealthStatus.HEALTHY if check(self.runtime) else HealthStatus.FAILED
        except Exception:
            return HealthStatus.FAILED

    def _overall(self, report: dict[str, HealthStatus]) -> HealthStatus:
        if not report:
            return HealthStatus.UNKNOWN

        statuses = report.values()

        if any(status == HealthStatus.FAILED for status in statuses):
            return HealthStatus.FAILED

        if self.runtime.lifecycle_state != RuntimeLifecycleState.READY:
            return HealthStatus.DEGRADED

        if any(status == HealthStatus.UNKNOWN for status in statuses):
            return HealthStatus.DEGRADED

        return HealthStatus.HEALTHY
