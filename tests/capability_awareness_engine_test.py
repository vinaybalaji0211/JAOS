from brain.capability_awareness_engine import CapabilityAwarenessEngine

engine = (
    CapabilityAwarenessEngine()
)

engine.register(
    "GitHub Integration",
    "JAOS v1 Alpha"
)

engine.register(
    "Robot Control",
    "JAOS v7"
)

engine.register(
    "IoT Automation",
    "JAOS v7"
)

supported, version = engine.check(
    "Robot Control"
)

print(
    supported,
    version
)

supported, version = engine.check(
    "Quantum Teleportation"
)

print(
    supported,
    version
)

engine.show_capabilities()