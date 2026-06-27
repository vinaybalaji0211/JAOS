from logs.logger import logger
from datetime import datetime


class ActionTimeline:

    def __init__(self):

        self.timeline = []

    def add_action(
            self,
            platform,
            module,
            action,
            result):

        self.timeline.append({

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "platform": platform,

            "module": module,

            "action": action,

            "result": result

        })

        logger.info(
            f"Timeline action: {action}"
        )

    def show_timeline(self):

        print("\n=== Action Timeline ===\n")

        if not self.timeline:

            print("No actions.")
            return

        for entry in self.timeline:

            print(entry["time"])

            print(f"  Platform : {entry['platform']}")

            print(f"  Module   : {entry['module']}")

            print(f"  Action   : {entry['action']}")

            print(f"  Result   : {entry['result']}")

            print()