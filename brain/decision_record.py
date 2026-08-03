import json
import os
from datetime import datetime, timezone

from logs.logger import logger


class DecisionRecord:

    FILE_PATH = "data/decisions/decision_records.json"

    @staticmethod
    def record(decision, reason, confidence):

        os.makedirs("data/decisions", exist_ok=True)

        records = DecisionRecord.get_all()

        records.append(
            {
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "decision": decision,
                "reason": reason,
                "confidence": confidence,
            }
        )

        with open(DecisionRecord.FILE_PATH, "w", encoding="utf-8") as file:

            json.dump(records, file, indent=4)

        logger.info(f"Decision recorded: {decision}")

    @staticmethod
    def get_all():

        if not os.path.exists(DecisionRecord.FILE_PATH):

            return []

        with open(DecisionRecord.FILE_PATH, "r", encoding="utf-8") as file:

            try:

                return json.load(file)

            except (json.JSONDecodeError, OSError):

                return []

    @staticmethod
    def show():

        records = DecisionRecord.get_all()

        print("\nDecision Records:")

        if not records:

            print("No decision records found.")

        else:

            for index, record in enumerate(records, start=1):

                print(f"{index}. [{record['timestamp']}]")

                print(f"Decision: {record['decision']}")

                print(f"Reason: {record['reason']}")

                print(f"Confidence: {record['confidence']}")
