import shutil

from logs.logger import logger


class ResourceAwarenessEngine:

    @staticmethod
    def assess_resources():

        total, used, free = shutil.disk_usage("/")

        resources = {

            "cpu_status": "NORMAL",

            "ram_status": "NORMAL",

            "gpu_status": "UNKNOWN",

            "internet_available": True,

            "disk_free_gb": round(
                free / (1024 ** 3),
                2
            )

        }

        logger.info(
            "Resource assessment completed."
        )

        return resources

    @staticmethod
    def show_resources():

        resources = (
            ResourceAwarenessEngine
            .assess_resources()
        )

        print("\nResource Awareness:\n")

        for key, value in resources.items():

            print(
                f"{key}: {value}"
            )
            