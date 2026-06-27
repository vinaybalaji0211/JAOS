from logs.logger import logger


class CloudKnowledgeSyncManager:

    def __init__(self):

        self.sync_records = []

    def sync(
            self,
            knowledge_item):

        record = {
            "item": knowledge_item,
            "status": "SYNCED"
        }

        self.sync_records.append(
            record
        )

        logger.info(
            f"Knowledge synced: "
            f"{knowledge_item}"
        )

    def show_sync_status(self):

        print(
            "\nCloud Knowledge Sync Manager:\n"
        )

        if not self.sync_records:

            print(
                "No synced knowledge."
            )

            return

        for record in self.sync_records:

            print(
                f"Item: "
                f"{record['item']}"
            )

            print(
                f"Status: "
                f"{record['status']}"
            )

            print()