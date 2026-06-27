from logs.logger import logger


class MemoryImportance:

    HIGH_PRIORITY_WORDS = [

        "error",

        "important",

        "critical",

        "phase",

        "goal",

        "warning"

    ]

    @staticmethod
    def calculate(memory):

        score = 1

        memory_lower = memory.lower()

        for word in MemoryImportance.HIGH_PRIORITY_WORDS:

            if word in memory_lower:

                score += 2

        logger.info(

            f"Importance score calculated: {score}"

        )

        return score