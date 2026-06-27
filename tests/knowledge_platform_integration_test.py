from knowledge.document_manager import DocumentManager
from knowledge.knowledge_base import KnowledgeBase
from knowledge.research_manager import ResearchManager
from knowledge.ocr_manager import OCRManager
from knowledge.knowledge_graph import KnowledgeGraph
from knowledge.learning_synchronizer import LearningSynchronizer

print("\n===== KNOWLEDGE PLATFORM TEST =====\n")

documents = DocumentManager()
documents.register_document(
    "JAOS Roadmap",
    "C:/JARVIS/docs/roadmap.pdf",
    "PDF"
)

knowledge = KnowledgeBase()
knowledge.add_entry(
    "JAOS",
    "AI Operating System"
)

research = ResearchManager()
research.register_project(
    "JAOS Research",
    "AI Operating Systems"
)

ocr = OCRManager()
ocr.register_job(
    "roadmap.pdf",
    "Extracted roadmap text..."
)

graph = KnowledgeGraph()
graph.add_relationship(
    "JAOS",
    "USES",
    "Knowledge Base"
)

sync = LearningSynchronizer()
sync.register_sync(
    "Knowledge Base",
    "Memory",
    "COMPLETED"
)

print("\n===== COMPONENT STATUS =====\n")

documents.show_documents()
knowledge.show_entries()
research.show_projects()
ocr.show_jobs()
graph.show_relationships()
sync.show_sync_jobs()

print("\n===== KNOWLEDGE PLATFORM COMPLETE =====")