from logs.logger import logger


class MemoryAgent:

    def __init__(self):

        self.name = "Memory Agent"

        self.memories = []

    def store_memory(
            self,
            memory,
            category="GENERAL",
            importance="NORMAL"):

        self.memories.append(
            {
                "memory": memory,
                "category": category,
                "importance": importance
            }
        )

        logger.info(
            "Memory stored."
        )

    def search_memory(
            self,
            keyword):

        results = []

        keyword = keyword.lower()

        for item in self.memories:

            if keyword in item[
                    "memory"
            ].lower():

                results.append(item)

        return results

    def show_memories(self):

        print(
            "\nMemory Agent:\n"
        )

        if not self.memories:

            print(
                "No memories stored."
            )

            return

        for index, item in enumerate(
                self.memories,
                start=1):

            print(
                f"{index}. "
                f"{item['memory']} | "
                f"{item['category']} | "
                f"{item['importance']}"
            )