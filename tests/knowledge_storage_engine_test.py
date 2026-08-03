from brain.knowledge_storage_engine import KnowledgeStorageEngine

engine = KnowledgeStorageEngine()

engine.store_entity(
    "Quantum Physics"
)

engine.store_entity(
    "JARVIS"
)

engine.store_relationship(
    {
        "source": "Vinay",
        "relation": "owns",
        "target": "JARVIS"
    }
)

engine.store_domain(
    "Physics"
)

engine.show_storage()