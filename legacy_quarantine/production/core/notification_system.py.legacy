from logs.logger import logger


class NotificationSystem:

    def __init__(self):

        self.notifications = []

    def notify(self, message):

        self.notifications.append(
            message
        )

        logger.info(
            f"Notification created: {message}"
        )

    def show_notifications(self):

        print("\nNotifications:")

        if not self.notifications:

            print("No notifications.")

        else:

            for index, notification in enumerate(
                    self.notifications,
                    start=1):

                print(
                    f"{index}. {notification}"
                )

    def clear_notifications(self):

        self.notifications.clear()

        logger.info(
            "Notifications cleared."
        )