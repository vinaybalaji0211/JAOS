from logs.logger import logger


class ToolAuditLogger:

    def __init__(self):

        self.audit_log = []

    def log_action(
            self,
            tool_name,
            action):

        record = {
            "tool": tool_name,
            "action": action
        }

        self.audit_log.append(
            record
        )

        logger.info(
            f"Audit logged: "
            f"{tool_name}"
        )

    def show_logs(self):

        print(
            "\nTool Audit Logger:\n"
        )

        if not self.audit_log:

            print(
                "No audit records."
            )

            return

        for record in self.audit_log:

            print(
                f"Tool: "
                f"{record['tool']}"
            )

            print(
                f"Action: "
                f"{record['action']}"
            )

            print()