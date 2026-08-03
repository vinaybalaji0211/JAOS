from brain.cloud_knowledge_sync_manager import CloudKnowledgeSyncManager

manager = (
    CloudKnowledgeSyncManager()
)

manager.sync(
    "Knowledge Graph"
)

manager.sync(
    "Skill Library"
)

manager.sync(
    "Evolution Memory"
)

manager.show_sync_status()