from brain.knowledge_conflict_detector import (
    KnowledgeConflictDetector
)


conflict_pairs = [

    {
        "source_1": "Memory",

        "value_1": "Internet available",

        "source_2": "Reality",

        "value_2": "Internet unavailable"
    },

    {
        "source_1": "Plan",

        "value_1": "Train huge model",

        "source_2": "Resources",

        "value_2": "RTX3050 4GB"
    },

    {
        "source_1": "Goal",

        "value_1": "Build AI OS",

        "source_2": "Task",

        "value_2": "Watch movie"
    }

]

KnowledgeConflictDetector.show_conflicts(
    conflict_pairs
)