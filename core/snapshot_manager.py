import json
import os
from datetime import datetime

from logs.logger import logger


class SnapshotManager:

    @staticmethod
    def create_snapshot(data):

        folder = "data/snapshots"

        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filepath = os.path.join(folder, f"{timestamp}.json")

        with open(filepath, "w") as file:

            json.dump(data, file, indent=4)

        logger.info(f"Snapshot created: {filepath}")

        print("Snapshot created:", filepath)