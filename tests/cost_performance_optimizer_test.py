from infrastructure.cost_performance_optimizer import (
    CostPerformanceOptimizer
)

optimizer = CostPerformanceOptimizer()

optimizer.register_resource(
    "OpenAI",
    20,
    95
)

optimizer.register_resource(
    "Gemini",
    10,
    90
)

optimizer.register_resource(
    "Local",
    0,
    70
)

optimizer.show_resources()

print(
    "\nRecommended:\n",
    optimizer.recommend()
)