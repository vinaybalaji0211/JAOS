from dashboard.platform_status_dashboard import PlatformStatusDashboard

dashboard = PlatformStatusDashboard()

dashboard.register_platform(
    "Security",
    "ONLINE",
    True
)

dashboard.register_platform(
    "Knowledge",
    "ONLINE",
    True
)

dashboard.register_platform(
    "Dashboard",
    "IN DEVELOPMENT",
    False
)

dashboard.show_platforms()