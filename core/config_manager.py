import json
import os

from logs.logger import logger


class ConfigManager:

    FILE_PATH = "config/settings.json"

    @staticmethod
    def load_config():

        if not os.path.exists(ConfigManager.FILE_PATH):

            default_config = {

                "jarvis_name": "JARVIS OS",

                "mode": "NORMAL",

                "ai_provider": "NONE"

            }

            os.makedirs("config", exist_ok=True)

            with open(
                    ConfigManager.FILE_PATH,
                    "w") as file:

                json.dump(
                    default_config,
                    file,
                    indent=4
                )

        with open(
                ConfigManager.FILE_PATH,
                "r") as file:

            config = json.load(file)

        logger.info(
            "Configuration loaded."
        )

        return config

    @staticmethod
    def save_config(config):

        with open(
                ConfigManager.FILE_PATH,
                "w") as file:

            json.dump(
                config,
                file,
                indent=4
            )

        logger.info(
            "Configuration updated."
        )