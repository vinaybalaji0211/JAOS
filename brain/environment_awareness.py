import os

from logs.logger import logger


class EnvironmentAwareness:

    @staticmethod
    def assess():

        environment = {

            "os_name": os.name,

            "current_directory": os.getcwd(),

            "python_version_available": True,

            "internet_available": True,

            "device_state": "NORMAL"

        }

        logger.info(
            "Environment assessment completed."
        )

        return environment

    @staticmethod
    def show_environment():

        env = EnvironmentAwareness.assess()

        print("\nEnvironment Awareness:\n")

        for key, value in env.items():

            print(
                f"{key}: {value}"
            )