import json
import os

from memory.long_term_memory import LongTermMemory
from memory.memory_importance import MemoryImportance
from logs.logger import logger


class MemoryCleanup:

    @staticmethod
    def clean(min_score=3):

        memories = LongTermMemory.get_all()

        cleaned = []

        removed = []

        for item in memories:

            score = MemoryImportance.calculate(
                item["memory"]
            )

            if score >= min_score:

                cleaned.append(item)

            else:

                removed.append(item)

        os.makedirs(
            "data/memory",
            exist_ok=True
        )

        with open(
                LongTermMemory.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                cleaned,
                file,
                indent=4
            )

        logger.info(
            f"Memory cleanup completed. Removed {len(removed)} memories."
        )

        return removed

    @staticmethod
    def show_cleanup(min_score=3):

        removed = MemoryCleanup.clean(
            min_score
        )

        print("\nMemory Cleanup:")

        if not removed:

            print("No memories removed.")

        else:

            print("Removed memories:")

            for index, item in enumerate(
                    removed,
                    start=1):

                print(
                    f"{index}. {item['memory']}"
                )