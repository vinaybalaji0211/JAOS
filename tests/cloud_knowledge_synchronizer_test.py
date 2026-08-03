from brain.cloud_knowledge_synchronizer import CloudKnowledgeSynchronizer

sync = (
    CloudKnowledgeSynchronizer()
)

sync.synchronize(
    "Knowledge Graph"
)

sync.synchronize(
    "Skill Library"
)

sync.synchronize(
    "Evolution Memory"
)

sync.show_history()