import psutil

from logs.logger import logger


class ResourceManager:

    @staticmethod
    def get_resources():

        resources = {

            "cpu_usage": psutil.cpu_percent(),

            "memory_usage": psutil.virtual_memory().percent,

            "disk_usage": psutil.disk_usage("/").percent

        }

        logger.info(
            "Resource information collected."
        )

        return resources

    @staticmethod
    def show_resources():

        resources = ResourceManager.get_resources()

        print("\nSystem Resources:")

        for key, value in resources.items():

            print(
                f"{key}: {value}%"
            )