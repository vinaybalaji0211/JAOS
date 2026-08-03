from datetime import datetime

from logs.logger import logger


class AuditLogger:

    def __init__(self):

        self.records = []

    def log_action(
            self,
            user,
            action,
            result):

        self.records.append({

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "user": user,

            "action": action,

            "result": result

        })

        logger.info(
            f"Audit: {user} -> {action}"
        )

    def show_records(self):

        print("\n=== Audit Logger ===\n")

        if not self.records:

            print("No audit records.")
            return

        for record in self.records:

            print(record["time"])
            print(f"  User   : {record['user']}")
            print(f"  Action : {record['action']}")
            print(f"  Result : {record['result']}")
            print()