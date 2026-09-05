from datetime import datetime

from logs.logger import logger


class NotificationCenter:

    def __init__(self):

        self.notifications = []

    def add_notification(
            self,
            source,
            title,
            priority="NORMAL"):

        self.notifications.append({

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "source": source,

            "title": title,

            "priority": priority,

            "read": False

        })

        logger.info(
            f"Notification added: {title}"
        )

    def show_notifications(self):

        print("\n=== Notification Center ===\n")

        if not self.notifications:

            print("No notifications.")
            return

        for notification in self.notifications:

            print(notification["time"])
            print(f"  Source   : {notification['source']}")
            print(f"  Title    : {notification['title']}")
            print(f"  Priority : {notification['priority']}")
            print(f"  Read     : {notification['read']}")
            print()