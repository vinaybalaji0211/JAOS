import json
import os
from datetime import datetime

from logs.logger import logger
from memory.long_term_memory import LongTermMemory


class MemoryExport:

    EXPORT_FOLDER = "exports"

    @staticmethod
    def export():

        os.makedirs(
            MemoryExport.EXPORT_FOLDER,
            exist_ok=True
        )

        memories = LongTermMemory.get_all()

        filename = (

            datetime.now().strftime(
                "memory_export_%Y%m%d_%H%M%S.json"
            )

        )

        path = os.path.join(

            MemoryExport.EXPORT_FOLDER,

            filename

        )

        with open(

                path,

                "w",

                encoding="utf-8"

        ) as file:

            json.dump(

                memories,

                file,

                indent=4

            )

        logger.info(

            f"Memory exported to {path}"

        )

        return path

    @staticmethod
    def show_export():

        path = MemoryExport.export()

        print(

            "\nMemory Export Successful"

        )

        print(

            f"Export file:\n{path}"

        )