from dashboard.mission_control import MissionControl
from jaos_platform.platform_runtime import PlatformRuntime


def test_mission_control_registers_with_runtime():
    runtime = PlatformRuntime()

    dashboard = MissionControl(runtime)

    assert runtime.container.resolve("mission_control") is dashboard


def test_mission_control_updates_runtime_context():
    runtime = PlatformRuntime()

    MissionControl(runtime)

    assert runtime.context.get("mission_control_status") == "READY"


def test_mission_control_defaults_still_work():
    runtime = PlatformRuntime()

    dashboard = MissionControl(runtime)

    assert dashboard.status == "ONLINE"
    assert dashboard.version == "JAOS v1 Alpha"