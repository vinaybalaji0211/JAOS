from datetime import datetime
from logs.logger import logger


class SecurityAuditSystem:

    def __init__(self):

        self.audit_log = []

    def log_event(
            self,
            action,
            decision,
            status):

        event = {

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "action": action,

            "decision": decision,

            "status": status

        }

        self.audit_log.append(
            event
        )

        logger.info(
            f"Security audit event logged: {action}"
        )

    def show_logs(self):

        print("\nSecurity Audit System:\n")

        if not self.audit_log:

            print(
                "No audit events."
            )

            return

        for index, event in enumerate(
                self.audit_log,
                start=1):

            print(
                f"{index}. "
                f"{event['timestamp']} | "
                f"{event['action']} | "
                f"{event['decision']} | "
                f"{event['status']}"
            )