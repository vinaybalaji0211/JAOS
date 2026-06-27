from dashboard.mission_control import MissionControl
from dashboard.platform_status_dashboard import PlatformStatusDashboard
from dashboard.capability_viewer import CapabilityViewer
from dashboard.notification_center import NotificationCenter
from dashboard.action_timeline import ActionTimeline
from dashboard.system_health_dashboard import SystemHealthDashboard

print("\n===== DASHBOARD PLATFORM TEST =====\n")

mission = MissionControl()

platforms = PlatformStatusDashboard()
platforms.register_platform(
    "Security",
    "ONLINE",
    True
)

capabilities = CapabilityViewer()
capabilities.register_capability(
    "Open VS Code",
    True,
    "v1 Alpha"
)

notifications = NotificationCenter()
notifications.add_notification(
    "Security",
    "Permission granted."
)

timeline = ActionTimeline()
timeline.add_action(
    "Development",
    "Git Manager",
    "Repository Registered",
    "SUCCESS"
)

health = SystemHealthDashboard()
health.update_status(
    "Security Platform",
    "HEALTHY"
)

mission.show_dashboard()

platforms.show_platforms()

capabilities.show_capabilities()

notifications.show_notifications()

timeline.show_timeline()

health.show_health()

print("\n===== DASHBOARD PLATFORM COMPLETE =====")