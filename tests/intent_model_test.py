from executive_brain.models.intent_model import IntentModel

intent = IntentModel(
    intent_type="OPEN_APPLICATION",
    confidence=0.98
)

intent.add_metadata(
    "application",
    "VS Code"
)

print()

print(intent.to_dict())