from logs.logger import logger


class TaskDelegationEngine:

    def __init__(self):

        self.delegations = []

    def delegate_task(
            self,
            task,
            from_agent,
            to_agent):

        delegation = {
            "task": task,
            "from": from_agent,
            "to": to_agent,
            "status": "DELEGATED"
        }

        self.delegations.append(
            delegation
        )

        logger.info(
            f"Task delegated: "
            f"{from_agent} -> {to_agent}"
        )

    def complete_task(
            self,
            task):

        for delegation in self.delegations:

            if delegation["task"] == task:

                delegation["status"] = (
                    "COMPLETED"
                )

    def show_delegations(self):

        print(
            "\nTask Delegation Engine:\n"
        )

        if not self.delegations:

            print(
                "No delegations."
            )

            return

        for delegation in self.delegations:

            print(
                f"Task: "
                f"{delegation['task']}"
            )

            print(
                f"From: "
                f"{delegation['from']}"
            )

            print(
                f"To: "
                f"{delegation['to']}"
            )

            print(
                f"Status: "
                f"{delegation['status']}"
            )

            print()