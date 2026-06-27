from knowledge.document_manager import (
    DocumentManager
)

manager = DocumentManager()

manager.register_document(
    "JAOS Roadmap",
    "C:/JARVIS/docs/roadmap.pdf",
    "PDF"
)

manager.register_document(
    "YOLO Notes",
    "C:/Projects/yolo_notes.md",
    "Markdown"
)

manager.show_documents()