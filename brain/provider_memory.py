import json
import os
from datetime import datetime

from logs.logger import logger


class ProviderMemory:

    FILE_PATH = "data/providers/provider_memory.json"

    @staticmethod
    def record_result(
            provider,
            task_type,
            result,
            notes=""):

        os.makedirs(
            "data/providers",
            exist_ok=True
        )

        records = ProviderMemory.get_all()

        records.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "provider": provider,
                "task_type": task_type,
                "result": result,
                "notes": notes
            }
        )

        with open(
                ProviderMemory.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                records,
                file,
                indent=4
            )

        logger.info(
            f"Provider result recorded: {provider}"
        )

    @staticmethod
    def get_all():

        if not os.path.exists(
                ProviderMemory.FILE_PATH):

            return []

        with open(
                ProviderMemory.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            try:

                return json.load(file)

            except:

                return []

    @staticmethod
    def show_memory():

        records = ProviderMemory.get_all()

        print("\nProvider Memory:")

        if not records:

            print("No provider memory found.")

        else:

            for index, record in enumerate(
                    records,
                    start=1):

                print(
                    f"{index}. [{record['timestamp']}] "
                    f"{record['provider']} | "
                    f"{record['task_type']} | "
                    f"{record['result']} | "
                    f"{record['notes']}"
                )