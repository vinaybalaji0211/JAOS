from brain.upgrade_impact_predictor import (
    UpgradeImpactPredictor
)

predictor = UpgradeImpactPredictor()

predictor.predict(
    "Cloud Memory Architecture",
    [
        "Persistent memory",
        "Backup protection",
        "Cross-device access"
    ],
    [
        "Cloud configuration required"
    ],
    "HIGH"
)

predictor.predict(
    "OCR Intelligence Engine",
    [
        "Document understanding",
        "Image text extraction"
    ],
    [
        "Additional dependencies"
    ],
    "MEDIUM"
)

predictor.show_predictions()