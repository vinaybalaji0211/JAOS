from brain.knowledge_validation_engine import KnowledgeValidationEngine

engine = (
    KnowledgeValidationEngine()
)

engine.validate(
    "Wikipedia",
    "Quantum Physics",
    82
)

engine.validate(
    "Unknown Blog",
    "Warp Drive",
    42
)

engine.validate(
    "MIT OpenCourseWare",
    "Wave Mechanics",
    97
)

engine.show_records()