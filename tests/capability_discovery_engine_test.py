from brain.capability_discovery_engine import (
    CapabilityDiscoveryEngine
)

engine = (
    CapabilityDiscoveryEngine()
)

engine.register_capability(
    "Research Analysis"
)

engine.register_capability(
    "Quantum Physics Expert",
    False
)

engine.show_capabilities()

print(
    engine.discover_gap(
        "Research Analysis"
    )
)

print(
    engine.discover_gap(
        "Quantum Physics Expert"
    )
)