from brain.digital_twin import DigitalTwin

DigitalTwin.show_simulation(
    plan_steps=[
        "Understand task",
        "Check resources",
        "Execute safely"
    ],
    resources_ok=True,
    risk_level="LOW",
    prediction_count=1,
    confidence=95
)

DigitalTwin.show_simulation(
    plan_steps=[
        "Train huge model"
    ],
    resources_ok=False,
    risk_level="HIGH",
    prediction_count=5,
    confidence=45
)