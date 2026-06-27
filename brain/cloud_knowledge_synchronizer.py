from logs.logger import logger


class CloudKnowledgeSynchronizer:

    def __init__(self):

        self.sync_history = []

    def synchronize(
            self,
            knowledge_item):

        record = {
            "knowledge": knowledge_item,
            "status": "SYNCHRONIZED"
        }

        self.sync_history.append(
            record
        )

        logger.info(
            f"Knowledge synchronized: "
            f"{knowledge_item}"
        )

    def show_history(self):

        print(
            "\nCloud Knowledge Synchronizer:\n"
        )

        if not self.sync_history:

            print(
                "No synchronization history."
            )

            return

        for record in self.sync_history:

            print(
                f"Knowledge: "
                f"{record['knowledge']}"
            )

            print(
                f"Status: "
                f"{record['status']}"
            )

            print()