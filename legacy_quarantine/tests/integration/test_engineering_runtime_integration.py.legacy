from engineering.platform_health_dashboard import (
    PlatformHealthDashboard,
)
from jaos_platform.platform_runtime import PlatformRuntime


def test_platform_health_dashboard_registers_with_runtime():
    runtime = PlatformRuntime()

    dashboard = PlatformHealthDashboard(runtime)

    assert (
        runtime.container.resolve(
            "platform_health_dashboard"
        )
        is dashboard
    )


def test_platform_health_dashboard_updates_runtime_context():
    runtime = PlatformRuntime()

    PlatformHealthDashboard(runtime)

    assert (
        runtime.context.get(
            "platform_health_dashboard_status"
        )
        == "READY"
    )


def test_platform_health_update_still_works():
    runtime = PlatformRuntime()

    dashboard = PlatformHealthDashboard(runtime)

    dashboard.update_platform(
        "Kernel",
        "100%",
        125,
        0,
        True,
    )

    assert dashboard.platforms["Kernel"]["health"] == "100%"
    assert dashboard.platforms["Kernel"]["passed"] == 125
    assert dashboard.platforms["Kernel"]["failed"] == 0
    assert dashboard.platforms["Kernel"]["certified"] is True