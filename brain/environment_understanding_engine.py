from logs.logger import logger


class EnvironmentUnderstandingEngine:

    def __init__(self):

        self.environment_data = {}

    def update_environment(
            self,
            key,
            value):

        self.environment_data[
            key
        ] = value

        logger.info(
            f"Environment updated: {key}"
        )

    def get_environment(
            self,
            key):

        return self.environment_data.get(
            key
        )

    def show_environment(self):

        print(
            "\nEnvironment Understanding Engine:\n"
        )

        if not self.environment_data:

            print(
                "No environment data."
            )

            return

        for key, value in (
                self.environment_data.items()):

            print(
                f"{key}: {value}"
            )