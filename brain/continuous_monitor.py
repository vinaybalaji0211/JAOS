from logs.logger import logger


class ContinuousMonitor:

    def __init__(self):

        self.monitored_items = {

            "system_health": "OK",

            "resources": "OK",

            "security": "OK",

            "plugins": "OK",

            "background_tasks": "OK"

        }

    def update_status(
            self,
            item,
            status):

        if item in self.monitored_items:

            self.monitored_items[item] = status

            logger.info(
                f"{item} status updated to {status}"
            )

    def show_status(self):

        print("\nContinuous Monitor:\n")

        for item, status in self.monitored_items.items():

            print(
                f"{item}: {status}"
            )