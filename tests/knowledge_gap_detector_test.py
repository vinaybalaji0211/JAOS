from brain.knowledge_gap_detector import KnowledgeGapDetector

detector = KnowledgeGapDetector()

detector.record_score(
    "Security",
    95
)

detector.record_score(
    "Planning",
    65
)

detector.record_score(
    "Long-Term Reasoning",
    60
)

detector.record_score(
    "Memory",
    90
)

detector.show_gaps()