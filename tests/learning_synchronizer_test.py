from knowledge.learning_synchronizer import (
    LearningSynchronizer
)

sync = LearningSynchronizer()

sync.register_sync(
    "Memory",
    "Knowledge Base"
)

sync.register_sync(
    "Knowledge Graph",
    "Learning Platform",
    "COMPLETED"
)

sync.show_sync_jobs()