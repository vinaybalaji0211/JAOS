from logs.logger import logger


class KnowledgeExtractionEngine:

    def __init__(self):

        self.extracted = []

    def extract(
            self,
            source,
            concepts):

        record = {
            "source": source,
            "concepts": concepts
        }

        self.extracted.append(
            record
        )

        logger.info(
            f"Knowledge extracted: {source}"
        )

    def show_extractions(self):

        print(
            "\nKnowledge Extraction Engine:\n"
        )

        if not self.extracted:

            print(
                "No extracted knowledge."
            )

            return

        for record in self.extracted:

            print(
                f"Source: {record['source']}"
            )

            print("Concepts:")

            for concept in record["concepts"]:

                print(
                    f" - {concept}"
                )

            print()