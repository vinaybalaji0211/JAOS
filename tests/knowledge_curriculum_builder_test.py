from brain.knowledge_curriculum_builder import (
    KnowledgeCurriculumBuilder
)

builder = (
    KnowledgeCurriculumBuilder()
)

builder.create_curriculum(
    "Quantum Physics",
    {
        "Level 1": [
            "Classical Physics",
            "Calculus"
        ],
        "Level 2": [
            "Wave Mechanics",
            "Linear Algebra"
        ],
        "Level 3": [
            "Quantum States",
            "Operators"
        ],
        "Level 4": [
            "Quantum Computing"
        ]
    }
)

builder.show_curriculum(
    "Quantum Physics"
)