from infrastructure.infrastructure_intelligence_core import (
    InfrastructureIntelligenceCore,
)

core = (
    InfrastructureIntelligenceCore()
)

core.register_component(
    "AI Provider Manager",
    "READY"
)

core.register_component(
    "Storage Intelligence",
    "READY"
)

core.register_component(
    "Database Intelligence",
    "PENDING"
)

core.show_components()