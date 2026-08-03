from logs.logger import logger
from memory.memory_search import MemorySearch


class MemoryReuse:

    @staticmethod
    def reuse(keyword):

        results = MemorySearch.search(
            keyword
        )

        logger.info(
            f"Memory reuse requested for: {keyword}"
        )

        return results

    @staticmethod
    def show_reuse(keyword):

        results = MemoryReuse.reuse(
            keyword
        )

        print(
            f"\nReusable Memories for '{keyword}':"
        )

        if not results:

            print(
                "No reusable memories found."
            )

        else:

            for index, item in enumerate(
                    results,
                    start=1):

                print(

                    f"{index}. "

                    f"{item['memory']}"

                )