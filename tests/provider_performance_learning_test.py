from brain.provider_performance_learning import (
    ProviderPerformanceLearning
)

learning = (
    ProviderPerformanceLearning()
)

learning.record(
    "OpenAI",
    "coding",
    True
)

learning.record(
    "OpenAI",
    "coding",
    True
)

learning.record(
    "Gemini",
    "coding",
    False
)

learning.record(
    "Gemini",
    "reasoning",
    True
)

learning.record(
    "Gemini",
    "reasoning",
    True
)

learning.show_stats()

print(
    "\nBest coding provider:",
    learning.best_provider(
        "coding"
    )
)

print(
    "Best reasoning provider:",
    learning.best_provider(
        "reasoning"
    )
)