from logs.logger import logger


class KnowledgeRetrievalEngine:

    def __init__(self):

        self.knowledge = []

    def add_knowledge(
            self,
            item):

        self.knowledge.append(
            item
        )

        logger.info(
            "Knowledge added."
        )

    def search(
            self,
            keyword):

        keyword = keyword.lower()

        results = []

        for item in self.knowledge:

            if keyword in str(
                    item).lower():

                results.append(
                    item
                )

        return results

    def show_search(
            self,
            keyword):

        results = self.search(
            keyword
        )

        print(
            "\nKnowledge Retrieval Engine:\n"
        )

        print(
            f"Keyword: {keyword}"
        )

        print(
            "\nResults:\n"
        )

        if not results:

            print(
                "No matches found."
            )

            return

        for item in results:

            print(item)