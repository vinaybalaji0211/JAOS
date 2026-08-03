from pc_control.notification_manager import NotificationManager

manager = NotificationManager()

manager.add_notification(
    "SUCCESS",
    "YOLO Training Completed"
)

manager.add_notification(
    "WARNING",
    "Battery Low"
)

manager.add_notification(
    "APPROVAL",
    "Delete duplicate files?"
)

manager.show_notifications()