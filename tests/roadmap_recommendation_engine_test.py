from brain.roadmap_recommendation_engine import (
    RoadmapRecommendationEngine
)

engine = (
    RoadmapRecommendationEngine()
)

engine.recommend(
    "Mobile Companion",
    "JAOS v3",
    "JAOS v2",
    "Requested frequently by the user."
)

engine.recommend(
    "Robot Control",
    "JAOS v7",
    "JAOS v7",
    "Current roadmap remains appropriate."
)

engine.show_recommendations()