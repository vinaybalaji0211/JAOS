from logs.logger import logger


class KnowledgeGraphCore:

    def __init__(self):

        self.entities = set()

        self.relationships = []

    def add_entity(
            self,
            entity):

        self.entities.add(entity)

        logger.info(
            f"Entity added: {entity}"
        )

    def add_relationship(
            self,
            source,
            relation,
            target):

        self.entities.add(source)
        self.entities.add(target)

        self.relationships.append(
            {
                "source": source,
                "relation": relation,
                "target": target
            }
        )

        logger.info(
            f"Relationship added: "
            f"{source} -> {relation} -> {target}"
        )

    def show_graph(self):

        print("\nKnowledge Graph Core:\n")

        print("Entities:\n")

        for entity in sorted(
                self.entities):

            print(
                f"- {entity}"
            )

        print("\nRelationships:\n")

        for rel in self.relationships:

            print(
                f"{rel['source']} "
                f"--{rel['relation']}--> "
                f"{rel['target']}"
            )