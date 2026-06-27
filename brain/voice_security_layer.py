from logs.logger import logger


class VoiceSecurityLayer:

    def __init__(self):

        self.protected_commands = [

            "SHUTDOWN",
            "DELETE_MEMORY",
            "SECURITY_ACCESS",
            "MODIFY_SETTINGS"
        ]

    def validate(
            self,
            role,
            command):

        command = command.upper()

        if command in self.protected_commands:

            if role != "AUTHOR":

                logger.warning(
                    f"Blocked command: "
                    f"{command}"
                )

                return False

        logger.info(
            f"Command allowed: {command}"
        )

        return True

    def show_validation(
            self,
            role,
            command):

        result = self.validate(
            role,
            command
        )

        print(
            "\nVoice Security Layer:\n"
        )

        print(
            f"Role: {role}"
        )

        print(
            f"Command: {command}"
        )

        print(
            f"Allowed: {result}"
        )