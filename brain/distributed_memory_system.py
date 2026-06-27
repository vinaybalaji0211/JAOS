from logs.logger import logger


class DistributedMemorySystem:

    def __init__(self):

        self.nodes = {}

    def add_node(
            self,
            node_name):

        self.nodes[
            node_name
        ] = []

        logger.info(
            f"Memory node added: "
            f"{node_name}"
        )

    def store(
            self,
            node_name,
            memory_item):

        if node_name in self.nodes:

            self.nodes[
                node_name
            ].append(
                memory_item
            )

    def show_nodes(self):

        print(
            "\nDistributed Memory System:\n"
        )

        if not self.nodes:

            print(
                "No memory nodes."
            )

            return

        for node, items in (
                self.nodes.items()):

            print(
                f"Node: {node}"
            )

            print(
                f"Items: {items}"
            )

            print()