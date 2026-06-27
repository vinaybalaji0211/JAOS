from logs.logger import logger


class KnowledgeGraph:

    def __init__(self):

        self.relationships = []

    def add_relationship(
            self,
            source,
            relation,
            target):

        self.relationships.append({
            "source": source,
            "relation": relation,
            "target": target
        })

        logger.info(
            f"Relationship added: {source}"
        )

    def show_relationships(self):

        print("\n=== Knowledge Graph ===\n")

        if not self.relationships:

            print("No relationships.")
            return

        for rel in self.relationships:

            print(
                f"{rel['source']} "
                f"--{rel['relation']}--> "
                f"{rel['target']}"
            )