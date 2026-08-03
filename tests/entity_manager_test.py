from brain.entity_manager import EntityManager

manager = EntityManager()

manager.add_entity(
    "Quantum Physics",
    "KNOWLEDGE_DOMAIN",
    {
        "difficulty": "HIGH",
        "status": "LEARNING"
    }
)

manager.add_entity(
    "JARVIS",
    "SYSTEM",
    {
        "version": "1.0"
    }
)

manager.update_entity(
    "JARVIS",
    {
        "phase": "Knowledge Graph"
    }
)

manager.show_entities()

print(
    manager.search_entity(
        "Quantum Physics"
    )
)