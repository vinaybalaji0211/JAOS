from brain.knowledge_acquisition_core import (
    KnowledgeAcquisitionCore
)

core = (
    KnowledgeAcquisitionCore()
)

core.acquire(
    "WEBSITE",
    "Wikipedia Quantum Physics"
)

core.acquire(
    "PDF",
    "Quantum Mechanics Notes"
)

core.acquire(
    "RESEARCH_PAPER",
    "Quantum Computing Paper"
)

core.show_sources()