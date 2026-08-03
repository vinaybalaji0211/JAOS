from brain.knowledge_gap_mapper import KnowledgeGapMapper

mapper = KnowledgeGapMapper()

mapper.define_domain(
    "Physics",
    [
        "Quantum Physics",
        "Electromagnetism",
        "Thermodynamics",
        "Relativity"
    ]
)

mapper.add_known_topic(
    "Physics",
    "Quantum Physics"
)

mapper.show_gaps(
    "Physics"
)