from jaos_platform.health_status import HealthStatus
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_health_certifier import (
    RuntimeHealthCertifier,
)


def test_runtime_health_reports_overall_healthy():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["overall"] == HealthStatus.HEALTHY


def test_runtime_health_reports_service_health():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["service_container"] == HealthStatus.HEALTHY


def test_runtime_health_reports_all_services():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert len(report) >= 5


def test_runtime_health_reports_unknown_overall_before_start():
    runtime = PlatformRuntime()

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report == {"overall": HealthStatus.UNKNOWN}


def test_runtime_health_reports_unknown_for_unrecognized_service():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()
    runtime.container.register("extra_service", object())

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["extra_service"] == HealthStatus.UNKNOWN
    assert report["overall"] == HealthStatus.DEGRADED


def test_runtime_health_reports_failed_for_missing_service_instance():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()
    runtime.context = None

    certifier = RuntimeHealthCertifier(runtime)

    report = certifier.certify()

    assert report["runtime_context"] == HealthStatus.FAILED
    assert report["overall"] == HealthStatus.FAILED