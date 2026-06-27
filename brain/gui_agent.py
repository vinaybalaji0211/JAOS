from logs.logger import logger


class GUIAgent:

    def __init__(self):

        self.supported_actions = [

            "click",

            "type",

            "read",

            "open",

            "close",

            "submit"

        ]

    def execute(
            self,
            action,
            target):

        if action not in self.supported_actions:

            result = (
                "Unsupported action."
            )

        else:

            result = (
                f"Simulated {action} on {target}"
            )

        logger.info(
            f"GUI action: {action}"
        )

        return result

    def show_capabilities(self):

        print("\nGUI Agent:\n")

        print(
            "Supported Actions:"
        )

        for action in self.supported_actions:

            print(
                f"- {action}"
            )