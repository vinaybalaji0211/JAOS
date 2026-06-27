from logs.logger import logger


class TerminalController:

    def __init__(self):

        self.commands = []

    def register_command(
            self,
            command):

        self.commands.append(command)

        logger.info(
            f"Terminal command registered: {command}"
        )

    def show_commands(self):

        print(
            "\n=== Terminal Controller ===\n"
        )

        if not self.commands:

            print(
                "No commands."
            )

            return

        for command in self.commands:

            print(command)