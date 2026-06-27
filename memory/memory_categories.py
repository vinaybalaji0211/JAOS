from logs.logger import logger


class MemoryCategories:

    CATEGORIES = {
        "project": [
            "phase",
            "step",
            "jarvis",
            "architecture"
        ],
        "user": [
            "user",
            "preference",
            "habit",
            "goal"
        ],
        "error": [
            "error",
            "bug",
            "failed",
            "warning"
        ],
        "system": [
            "cpu",
            "memory",
            "disk",
            "resource"
        ],
        "task": [
            "task",
            "schedule",
            "action",
            "workflow"
        ]
    }

    @staticmethod
    def classify(memory):

        memory_lower = memory.lower()

        for category, keywords in MemoryCategories.CATEGORIES.items():

            for keyword in keywords:

                if keyword in memory_lower:

                    logger.info(
                        f"Memory classified as: {category}"
                    )

                    return category

        logger.info(
            "Memory classified as: general"
        )

        return "general"

    @staticmethod
    def show_category(memory):

        category = MemoryCategories.classify(memory)

        print("\nMemory Category:")

        print(category)