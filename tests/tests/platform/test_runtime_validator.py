from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_validator import RuntimeValidator


def test_runtime_validator_reports_healthy_runtime():
    runtime = PlatformRuntime()

    validator = RuntimeValidator(runtime)

    report = validator.validate()

    assert report["healthy"] is True


def test_runtime_validator_checks_container():
    runtime = PlatformRuntime()

    validator = RuntimeValidator(runtime)

    report = validator.validate()

    assert report["container"] is True


def test_runtime_validator_checks_context():
    runtime = PlatformRuntime()

    validator = RuntimeValidator(runtime)

    report = validator.validate()

    assert report["context"] is True


def test_runtime_validator_checks_event_bus():
    runtime = PlatformRuntime()

    validator = RuntimeValidator(runtime)

    report = validator.validate()

    assert report["event_bus"] is True


def test_runtime_validator_checks_service_registry():
    runtime = PlatformRuntime()

    validator = RuntimeValidator(runtime)

    report = validator.validate()

    assert report["services"] is True