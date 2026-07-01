from jaos_platform.platform_runtime import PlatformRuntime
from security.security_monitor import SecurityMonitor


def test_security_monitor_registers_with_runtime():
    runtime = PlatformRuntime()

    security = SecurityMonitor(runtime)

    assert runtime.container.resolve("security_monitor") is security


def test_security_monitor_updates_runtime_context():
    runtime = PlatformRuntime()

    SecurityMonitor(runtime)

    assert runtime.context.get("security_monitor_status") == "READY"


def test_security_event_recording_still_works():
    runtime = PlatformRuntime()

    security = SecurityMonitor(runtime)
    security.record_event("INFO", "Test event")

    assert security.events == [
        {
            "level": "INFO",
            "description": "Test event",
        }
    ]