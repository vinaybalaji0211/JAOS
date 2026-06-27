from brain.upgrade_recommendation_engine import (
    UpgradeRecommendationEngine
)

engine = UpgradeRecommendationEngine()

engine.recommend_upgrade(
    "Cloud Memory Missing",
    "Cloud Memory Architecture",
    "Persistent memory and backup"
)

engine.recommend_upgrade(
    "OCR Missing",
    "OCR Intelligence Engine",
    "Read images and documents"
)

engine.show_recommendations()