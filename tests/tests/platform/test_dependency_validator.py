from jaos_platform.dependency_validator import (
    DependencyValidator,
)
from jaos_platform.platform_runtime import PlatformRuntime


def test_dependency_validator_reports_valid():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    validator = DependencyValidator(runtime)

    report = validator.validate()

    assert report["valid"] is True


def test_dependency_validator_has_no_missing_services():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    validator = DependencyValidator(runtime)

    report = validator.validate()

    assert report["missing_services"] == []


def test_dependency_validator_counts_services():
    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    validator = DependencyValidator(runtime)

    report = validator.validate()

    assert report["registered_services"] >= 4