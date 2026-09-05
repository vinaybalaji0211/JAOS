from logs.logger import logger


class NotificationManager:

    def __init__(self):

        self.notifications = []

    def add_notification(
            self,
            level,
            message):

        self.notifications.append(
            {
                "level": level,
                "message": message
            }
        )

        logger.info(
            f"Notification added: {level}"
        )

    def show_notifications(self):

        print(
            "\n=== Notification Manager ===\n"
        )

        if not self.notifications:

            print(
                "No notifications."
            )

            return

        for item in self.notifications:

            print(
                f"[{item['level']}] "
                f"{item['message']}"
            )