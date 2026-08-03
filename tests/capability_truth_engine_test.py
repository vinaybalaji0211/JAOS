from engineering.capability_truth_engine import CapabilityTruthEngine

engine = CapabilityTruthEngine()

engine.register_capability(
    "Open VS Code",
    "PC Control",
    True,
    "v1 Alpha"
)

engine.register_capability(
    "Autonomous Self Improvement",
    "AI Core",
    False,
    "v2.0",
    "Planned feature"
)

engine.show_capabilities()

print()

print(
    engine.can_execute(
        "Open VS Code"
    )
)