from logs.logger import logger


class ConfigurationManager:

    def __init__(self):

        self.config = {}

    def set_value(
            self,
            key,
            value):

        self.config[key] = value

        logger.info(
            f"Configuration updated: {key}"
        )

    def get_value(
            self,
            key):

        return self.config.get(key)

    def show_config(self):

        print("\n=== Configuration Manager ===\n")

        if not self.config:

            print("No configuration values.")
            return

        for key, value in self.config.items():

            print(f"{key} : {value}")