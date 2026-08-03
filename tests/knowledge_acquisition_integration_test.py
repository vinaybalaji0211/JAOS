from brain.knowledge_acquisition_core import KnowledgeAcquisitionCore
from brain.knowledge_extraction_engine import KnowledgeExtractionEngine
from brain.knowledge_validation_engine import KnowledgeValidationEngine
from brain.research_paper_learning_engine import ResearchPaperLearningEngine
from brain.resource_discovery_engine import ResourceDiscoveryEngine
from brain.web_learning_engine import WebLearningEngine

print(
    "\n=== KNOWLEDGE ACQUISITION INTEGRATION TEST ===\n"
)

# Acquisition
acquisition = KnowledgeAcquisitionCore()

acquisition.acquire(
    "WEBSITE",
    "MIT OpenCourseWare"
)

acquisition.acquire(
    "RESEARCH_PAPER",
    "Attention Is All You Need"
)

acquisition.show_sources()

# Discovery
discovery = ResourceDiscoveryEngine()

discovery.add_resource(
    "Artificial Intelligence",
    "MIT OpenCourseWare"
)

discovery.add_resource(
    "Artificial Intelligence",
    "Attention Is All You Need"
)

discovery.show_resources()

# Web Learning
web = WebLearningEngine()

web.learn(
    "MIT OpenCourseWare",
    "Neural Networks"
)

web.show_learning()

# Research Learning
papers = ResearchPaperLearningEngine()

papers.learn_paper(
    "Attention Is All You Need",
    "Transformer Models"
)

papers.show_papers()

# Validation
validation = KnowledgeValidationEngine()

validation.validate(
    "MIT OpenCourseWare",
    "Neural Networks",
    98
)

validation.validate(
    "Unknown Blog",
    "Magic AI",
    25
)

validation.show_records()

# Extraction
extractor = KnowledgeExtractionEngine()

extractor.extract(
    "Attention Is All You Need",
    [
        "Transformer",
        "Self Attention",
        "Encoder",
        "Decoder"
    ]
)

extractor.show_extractions()

print(
    "\n=== KNOWLEDGE ACQUISITION COMPLETE ==="
)