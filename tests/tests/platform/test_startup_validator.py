from jaos_platform.boot_manager import BootManager
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.startup_validator import StartupValidator


def test_startup_validator_reports_ready():
    runtime = PlatformRuntime()

    runtime.context.set("config_manager_status", "READY")
    runtime.context.set("executive_brain_status", "READY")
    runtime.context.set("startup_manager_status", "READY")

    BootManager(runtime).boot()

    validator = StartupValidator(runtime)

    report = validator.validate()

    assert report["ready"] is True


def test_boot_status_check():
    runtime = PlatformRuntime()

    BootManager(runtime).boot()

    validator = StartupValidator(runtime)

    assert validator.validate()["boot_status"] is True


def test_configuration_check():
    runtime = PlatformRuntime()

    runtime.context.set("config_manager_status", "READY")

    validator = StartupValidator(runtime)

    assert validator.validate()["configuration"] is True


def test_executive_check():
    runtime = PlatformRuntime()

    runtime.context.set("executive_brain_status", "READY")

    validator = StartupValidator(runtime)

    assert validator.validate()["executive_brain"] is True


def test_startup_services_check():
    runtime = PlatformRuntime()

    runtime.context.set("startup_manager_status", "READY")

    validator = StartupValidator(runtime)

    assert validator.validate()["startup_services"] is True