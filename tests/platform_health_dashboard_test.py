from engineering.platform_health_dashboard import PlatformHealthDashboard

dashboard = PlatformHealthDashboard()

dashboard.update_platform(
    "Security Platform",
    "HEALTHY",
    27,
    0,
    True
)

dashboard.update_platform(
    "Engineering Platform",
    "IN DEVELOPMENT",
    10,
    0,
    False
)

dashboard.show_dashboard()