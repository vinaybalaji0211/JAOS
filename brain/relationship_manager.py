from logs.logger import logger


class RelationshipManager:

    def __init__(self):

        self.relationships = []

    def add_relationship(
            self,
            source,
            relation,
            target,
            metadata=None):

        if metadata is None:
            metadata = {}

        self.relationships.append(
            {
                "source": source,
                "relation": relation,
                "target": target,
                "metadata": metadata
            }
        )

        logger.info(
            f"Relationship added: "
            f"{source} -> {relation} -> {target}"
        )

    def find_relationships(
            self,
            entity):

        results = []

        for rel in self.relationships:

            if (
                rel["source"] == entity
                or rel["target"] == entity
            ):
                results.append(rel)

        return results

    def show_relationships(self):

        print(
            "\nRelationship Manager:\n"
        )

        if not self.relationships:

            print(
                "No relationships."
            )

            return

        for rel in self.relationships:

            print(
                f"{rel['source']} "
                f"--{rel['relation']}--> "
                f"{rel['target']}"
            )

            print(
                f"Metadata: "
                f"{rel['metadata']}"
            )

            print()