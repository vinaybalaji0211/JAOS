from dashboard.system_health_dashboard import (
    SystemHealthDashboard
)

dashboard = SystemHealthDashboard()

dashboard.update_status(
    "Memory Platform",
    "HEALTHY"
)

dashboard.update_status(
    "Security Platform",
    "HEALTHY"
)

dashboard.update_status(
    "Dashboard Platform",
    "IN DEVELOPMENT"
)

dashboard.show_health()