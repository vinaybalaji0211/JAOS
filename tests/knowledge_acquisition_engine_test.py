from brain.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine
)

engine = KnowledgeAcquisitionEngine()

engine.acquire_subject(
    "Quantum Physics",
    "Physics"
)

engine.acquire_subject(
    "Cybersecurity",
    "Security"
)

engine.show_learning_targets()

engine.complete_subject(
    "Quantum Physics"
)

print("\nAfter Completion:\n")

engine.show_learning_targets()