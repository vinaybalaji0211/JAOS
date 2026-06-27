import json
import os

from logs.logger import logger


class RecoveryManager:

    @staticmethod
    def recover_latest_snapshot():

        folder = "data/snapshots"

        if not os.path.exists(folder):

            logger.warning("Snapshots folder does not exist.")

            return None

        files = os.listdir(folder)

        if not files:

            logger.warning("No snapshots found.")

            return None

        latest_file = max(
            [os.path.join(folder, file) for file in files],
            key=os.path.getctime
        )

        with open(latest_file, "r") as file:

            data = json.load(file)

        logger.info(f"Recovered snapshot: {latest_file}")

        return data