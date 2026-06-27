from brain.knowledge_retrieval_engine import (
    KnowledgeRetrievalEngine
)

engine = KnowledgeRetrievalEngine()

engine.add_knowledge(
    "Quantum Physics"
)

engine.add_knowledge(
    "Cloud Memory Architecture"
)

engine.add_knowledge(
    "Security Threat Response Engine"
)

engine.show_search(
    "cloud"
)

engine.show_search(
    "security"
)