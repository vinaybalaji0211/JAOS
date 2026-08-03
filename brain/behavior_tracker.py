import json
import os
from datetime import datetime, timezone

from logs.logger import logger


class BehaviorTracker:

    FILE_PATH = "data/behavior/behavior_patterns.json"

    @staticmethod
    def record_behavior(behavior):

        os.makedirs("data/behavior", exist_ok=True)

        behaviors = BehaviorTracker.get_behaviors()

        behaviors.append(
            {
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "behavior": behavior,
            }
        )

        with open(BehaviorTracker.FILE_PATH, "w", encoding="utf-8") as file:

            json.dump(behaviors, file, indent=4)

        logger.info(f"Behavior recorded: {behavior}")

    @staticmethod
    def get_behaviors():

        if not os.path.exists(BehaviorTracker.FILE_PATH):

            return []

        with open(BehaviorTracker.FILE_PATH, "r", encoding="utf-8") as file:

            try:

                return json.load(file)

            except (json.JSONDecodeError, OSError):

                return []

    @staticmethod
    def show_behaviors():

        behaviors = BehaviorTracker.get_behaviors()

        print("\nBehavior Patterns:")

        if not behaviors:

            print("No behavior patterns recorded.")

        else:

            for index, item in enumerate(behaviors, start=1):

                print(f"{index}. [{item['timestamp']}] {item['behavior']}")
