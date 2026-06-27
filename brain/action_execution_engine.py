from logs.logger import logger


class ActionExecutionEngine:

    def __init__(self):

        self.execution_history = []

    def execute(
            self,
            action_name,
            result):

        record = {
            "action": action_name,
            "result": result,
            "status": "EXECUTED"
        }

        self.execution_history.append(
            record
        )

        logger.info(
            f"Action executed: "
            f"{action_name}"
        )

        return result

    def show_history(self):

        print(
            "\nAction Execution Engine:\n"
        )

        if not self.execution_history:

            print(
                "No executions."
            )

            return

        for record in (
                self.execution_history):

            print(
                f"Action: "
                f"{record['action']}"
            )

            print(
                f"Result: "
                f"{record['result']}"
            )

            print(
                f"Status: "
                f"{record['status']}"
            )

            print()