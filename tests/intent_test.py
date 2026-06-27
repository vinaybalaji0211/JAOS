from executive_brain.intent import Intent

intent = Intent(
    intent_type="OPEN_APPLICATION"
)

intent.add_metadata(
    "application",
    "VS Code"
)

intent.add_metadata(
    "confidence",
    0.99
)

intent.show()