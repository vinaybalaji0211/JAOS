from logs.logger import logger
from memory.long_term_memory import LongTermMemory


class MemorySearch:

    @staticmethod
    def search(keyword):

        results = []

        memories = LongTermMemory.get_all()

        keyword = keyword.lower()

        for item in memories:

            if keyword in item["memory"].lower():

                results.append(item)

        logger.info(
            f"Memory search performed for: {keyword}"
        )

        return results

    @staticmethod
    def show_results(keyword):

        results = MemorySearch.search(
            keyword
        )

        print(
            f"\nSearch Results for '{keyword}':"
        )

        if not results:

            print(
                "No matching memories found."
            )

        else:

            for index, item in enumerate(
                    results,
                    start=1):

                print(
                    f"{index}. [{item['timestamp']}] {item['memory']}"
                )