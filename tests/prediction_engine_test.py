from brain.prediction_engine import PredictionEngine

PredictionEngine.show_predictions(
    resources_ok=False,
    capability_available=False,
    risk_level="HIGH",
    conflict_count=2,
    confidence=45
)

PredictionEngine.show_predictions(
    resources_ok=True,
    capability_available=True,
    risk_level="LOW",
    conflict_count=0,
    confidence=95
)