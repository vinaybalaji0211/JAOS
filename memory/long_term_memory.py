import json
import os
from datetime import datetime

from logs.logger import logger


class LongTermMemory:

    FILE_PATH = "data/memory/long_term_memory.json"

    @staticmethod
    def add(memory):

        os.makedirs(
            "data/memory",
            exist_ok=True
        )

        memories = LongTermMemory.get_all()

        memories.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "memory": memory
            }
        )

        with open(
                LongTermMemory.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                memories,
                file,
                indent=4
            )

        logger.info(
            f"Long-term memory added: {memory}"
        )

    @staticmethod
    def get_all():

        if not os.path.exists(
                LongTermMemory.FILE_PATH):

            return []

        with open(
                LongTermMemory.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            try:

                return json.load(file)

            except:

                return []

    @staticmethod
    def show():

        memories = LongTermMemory.get_all()

        print("\nLong-Term Memory:")

        if not memories:

            print("No long-term memories.")

        else:

            for index, item in enumerate(
                    memories,
                    start=1):

                print(
                    f"{index}. [{item['timestamp']}] {item['memory']}"
                )