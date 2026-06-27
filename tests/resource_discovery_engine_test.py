from brain.resource_discovery_engine import (
    ResourceDiscoveryEngine
)

engine = (
    ResourceDiscoveryEngine()
)

engine.add_resource(
    "Quantum Physics",
    "MIT Quantum Notes"
)

engine.add_resource(
    "Quantum Physics",
    "Quantum Computing Paper"
)

engine.add_resource(
    "Quantum Physics",
    "University Lecture Series"
)

engine.show_resources()

print(
    engine.get_resources(
        "Quantum Physics"
    )
)