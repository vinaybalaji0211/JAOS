from core.notification_system import NotificationSystem


notifications = NotificationSystem()

notifications.notify(
    "JARVIS OS started successfully."
)

notifications.notify(
    "Capability registry loaded."
)

notifications.notify(
    "System resources checked."
)

notifications.show_notifications()