from logs.logger import logger


class EnvironmentGraph:

    def __init__(self):

        self.relationships = []

    def add_relationship(
            self,
            source,
            relation,
            target):

        relationship = {

            "source": source,

            "relation": relation,

            "target": target

        }

        self.relationships.append(
            relationship
        )

        logger.info(
            f"{source} {relation} {target}"
        )

    def get_relationships(
            self,
            entity):

        result = []

        for relation in self.relationships:

            if (
                    relation["source"] == entity
                    or relation["target"] == entity):

                result.append(
                    relation
                )

        return result

    def show_graph(self):

        print("\nEnvironment Graph:\n")

        if not self.relationships:

            print(
                "Graph empty."
            )

            return

        for relation in self.relationships:

            print(

                f"{relation['source']} "

                f"--{relation['relation']}--> "

                f"{relation['target']}"

            )