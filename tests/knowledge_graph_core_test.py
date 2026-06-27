from brain.knowledge_graph_core import (
    KnowledgeGraphCore
)

graph = KnowledgeGraphCore()

graph.add_entity(
    "Vinay"
)

graph.add_entity(
    "JARVIS"
)

graph.add_relationship(
    "Vinay",
    "owns",
    "JARVIS"
)

graph.add_relationship(
    "JARVIS",
    "contains",
    "Security Agent"
)

graph.add_relationship(
    "Security Agent",
    "protects",
    "Cloud Memory"
)

graph.show_graph()