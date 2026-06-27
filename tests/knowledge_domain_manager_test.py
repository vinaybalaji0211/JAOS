from brain.knowledge_domain_manager import (
    KnowledgeDomainManager
)


manager = KnowledgeDomainManager()

manager.add_domain(
    "Physics",
    "Study of matter, energy, and fundamental laws."
)

manager.add_topic(
    "Physics",
    "Quantum Physics"
)

manager.add_topic(
    "Physics",
    "Electromagnetism"
)

manager.add_domain(
    "Cybersecurity",
    "Protection of systems, data, and networks."
)

manager.add_topic(
    "Cybersecurity",
    "Threat Detection"
)

manager.show_domains()