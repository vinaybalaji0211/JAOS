from logs.logger import logger


class VoiceCommandPrioritizer:

    PRIORITY_ORDER = {
        "EMERGENCY": 0,
        "SECURITY": 1,
        "AUTHOR": 2,
        "NORMAL": 3,
        "BACKGROUND": 4
    }

    def __init__(self):
        self.commands = []

    def add_command(
            self,
            command,
            command_type):

        item = {
            "command": command,
            "type": command_type
        }

        self.commands.append(item)

        self.commands.sort(
            key=lambda x: self.PRIORITY_ORDER.get(
                x["type"],
                99
            )
        )

        logger.info(
            f"Voice command prioritized: {command}"
        )

    def show_commands(self):

        print("\nVoice Command Prioritizer:\n")

        if not self.commands:
            print("No commands.")
            return

        for index, item in enumerate(
                self.commands,
                start=1):

            print(
                f"{index}. "
                f"{item['command']} | "
                f"{item['type']}"
            )