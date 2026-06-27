from logs.logger import logger


class EntityManager:

    def __init__(self):

        self.entities = {}

    def add_entity(
            self,
            entity_name,
            entity_type="GENERAL",
            metadata=None):

        if metadata is None:
            metadata = {}

        self.entities[entity_name] = {
            "type": entity_type,
            "metadata": metadata
        }

        logger.info(
            f"Entity added: {entity_name}"
        )

    def update_entity(
            self,
            entity_name,
            metadata):

        if entity_name in self.entities:

            self.entities[
                entity_name
            ]["metadata"].update(
                metadata
            )

            logger.info(
                f"Entity updated: {entity_name}"
            )

    def remove_entity(
            self,
            entity_name):

        if entity_name in self.entities:

            del self.entities[
                entity_name
            ]

            logger.info(
                f"Entity removed: {entity_name}"
            )

    def search_entity(
            self,
            entity_name):

        return self.entities.get(
            entity_name
        )

    def show_entities(self):

        print("\nEntity Manager:\n")

        if not self.entities:

            print("No entities.")

            return

        for name, details in (
                self.entities.items()):

            print(
                f"Entity: {name}"
            )

            print(
                f"Type: {details['type']}"
            )

            print(
                f"Metadata: "
                f"{details['metadata']}"
            )

            print()