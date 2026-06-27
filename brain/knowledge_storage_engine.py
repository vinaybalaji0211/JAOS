from logs.logger import logger


class KnowledgeStorageEngine:

    def __init__(self):

        self.storage = {
            "entities": [],
            "relationships": [],
            "domains": []
        }

    def store_entity(
            self,
            entity):

        self.storage[
            "entities"
        ].append(entity)

        logger.info(
            f"Stored entity: {entity}"
        )

    def store_relationship(
            self,
            relationship):

        self.storage[
            "relationships"
        ].append(
            relationship
        )

        logger.info(
            "Stored relationship."
        )

    def store_domain(
            self,
            domain):

        self.storage[
            "domains"
        ].append(domain)

        logger.info(
            f"Stored domain: {domain}"
        )

    def show_storage(self):

        print(
            "\nKnowledge Storage Engine:\n"
        )

        for key, value in (
                self.storage.items()):

            print(
                f"{key.upper()}:"
            )

            print(value)

            print()