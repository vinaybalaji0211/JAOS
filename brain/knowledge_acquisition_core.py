from logs.logger import logger


class KnowledgeAcquisitionCore:

    def __init__(self):

        self.sources = []

    def acquire(
            self,
            source_type,
            source_name):

        record = {
            "type": source_type,
            "source": source_name
        }

        self.sources.append(
            record
        )

        logger.info(
            f"Knowledge acquired: "
            f"{source_name}"
        )

    def show_sources(self):

        print(
            "\nKnowledge Acquisition Core:\n"
        )

        if not self.sources:

            print(
                "No knowledge sources."
            )

            return

        for source in self.sources:

            print(
                f"Type: "
                f"{source['type']}"
            )

            print(
                f"Source: "
                f"{source['source']}"
            )

            print()