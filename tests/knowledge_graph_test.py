from knowledge.knowledge_graph import (
    KnowledgeGraph
)

graph = KnowledgeGraph()

graph.add_relationship(
    "JAOS",
    "USES",
    "GitHub"
)

graph.add_relationship(
    "JAOS",
    "USES",
    "VS Code"
)

graph.add_relationship(
    "YOLO Project",
    "HAS_DOCUMENT",
    "Research Paper"
)

graph.show_relationships()