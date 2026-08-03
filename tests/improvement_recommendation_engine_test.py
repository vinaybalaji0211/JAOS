from brain.improvement_recommendation_engine import ImprovementRecommendationEngine

ImprovementRecommendationEngine.show_recommendations(
    weaknesses=[
        "Threat monitoring",
        "Long-term planning"
    ],
    failures=[
        "Plugin timeout",
        "Memory overload"
    ],
    low_scores={
        "Planning": 65,
        "Recovery": 70
    }
)