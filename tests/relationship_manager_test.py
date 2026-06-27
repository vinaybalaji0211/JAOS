from brain.relationship_manager import (
    RelationshipManager
)

manager = RelationshipManager()

manager.add_relationship(
    "Vinay",
    "owns",
    "JARVIS"
)

manager.add_relationship(
    "JARVIS",
    "contains",
    "Security Agent"
)

manager.add_relationship(
    "Security Agent",
    "protects",
    "Cloud Memory",
    {
        "priority": "HIGH"
    }
)

manager.show_relationships()

print(
    "\nRelationships for JARVIS:\n"
)

for rel in manager.find_relationships(
        "JARVIS"):

    print(rel)