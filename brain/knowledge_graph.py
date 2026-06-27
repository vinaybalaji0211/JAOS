from logs.logger import logger


class KnowledgeGraph:

    def __init__(self):

        self.nodes = []

        self.edges = []

    def add_node(self, name, node_type):

        node = {

            "name": name,

            "type": node_type

        }

        if node not in self.nodes:

            self.nodes.append(node)

            logger.info(
                f"Node added: {name}"
            )

    def add_edge(

            self,

            source,

            relation,

            target):

        edge = {

            "source": source,

            "relation": relation,

            "target": target

        }

        if edge not in self.edges:

            self.edges.append(edge)

            logger.info(
                f"Edge added: {source} {relation} {target}"
            )

    def show_nodes(self):

        print("\nKnowledge Graph Nodes:")

        for node in self.nodes:

            print(node)

    def show_edges(self):

        print("\nKnowledge Graph Edges:")

        for edge in self.edges:

            print(edge)