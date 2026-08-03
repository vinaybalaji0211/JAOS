from dashboard.notification_center import NotificationCenter

center = NotificationCenter()

center.add_notification(
    "Security",
    "Permission granted."
)

center.add_notification(
    "Development",
    "Build completed successfully.",
    "HIGH"
)

center.show_notifications()