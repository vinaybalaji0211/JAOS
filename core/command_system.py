from logs.logger import logger


class CommandSystem:

    @staticmethod
    def process(command):

        logger.info(
            f"Command received: {command}"
        )

        command = command.lower()

        if command == "status":

            return "JARVIS OS is online."

        elif command == "hello":

            return "Hello sir, I am JARVIS."

        elif command == "exit":

            return "Goodbye sir."

        else:

            return "Unknown command."