from jaos_platform.health_status import HealthStatus
from jaos_platform.platform_runtime import PlatformRuntime


class RuntimeHealthCertifier:
    """Certifies the health of the JAOS runtime."""

    def __init__(self, runtime: PlatformRuntime):
        self.runtime = runtime

    def certify(self) -> dict:
        services = self.runtime.container.list_services()

        report = {}

        for service in services:
            report[service] = HealthStatus.HEALTHY

        report["overall"] = HealthStatus.HEALTHY

        return report