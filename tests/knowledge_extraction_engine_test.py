from brain.knowledge_extraction_engine import KnowledgeExtractionEngine

engine = (
    KnowledgeExtractionEngine()
)

engine.extract(
    "Attention Is All You Need",
    [
        "Transformer",
        "Self Attention",
        "Encoder",
        "Decoder",
        "Positional Encoding"
    ]
)

engine.extract(
    "Quantum Computing Paper",
    [
        "Qubit",
        "Superposition",
        "Entanglement",
        "Quantum Gate"
    ]
)

engine.show_extractions()