from knowledge.knowledge_base import (
    KnowledgeBase
)

kb = KnowledgeBase()

kb.add_entry(
    "YOLO",
    "Real-time object detection framework."
)

kb.add_entry(
    "JAOS",
    "AI Operating System project."
)

kb.show_entries()