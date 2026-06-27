import json
import os
from datetime import datetime

from logs.logger import logger


class ActionHistory:

    FILE_PATH = "data/history/actions.json"

    @staticmethod
    def record_action(action):

        os.makedirs("data/history", exist_ok=True)

        actions = []

        if os.path.exists(ActionHistory.FILE_PATH):

            with open(ActionHistory.FILE_PATH, "r") as file:

                try:

                    actions = json.load(file)

                except:

                    actions = []

        actions.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action
            }
        )

        with open(ActionHistory.FILE_PATH, "w") as file:

            json.dump(actions, file, indent=4)

        logger.info(f"Action recorded: {action}")