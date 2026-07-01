from jaos_platform.health_status import HealthStatus
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_health_certifier import (
    RuntimeHealthCertifier,
)


def test_runtime_health_reports_overall_healthy():
    runtime = PlatformRuntime()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["overall"] == HealthStatus.HEALTHY


def test_runtime_health_reports_service_health():
    runtime = PlatformRuntime()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["service_container"] == HealthStatus.HEALTHY


def test_runtime_health_reports_all_services():
    runtime = PlatformRuntime()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert len(report) >= 5