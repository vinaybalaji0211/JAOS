from brain.capability_matching_engine import (
    CapabilityMatchingEngine
)


required_capabilities = [
    "planning",
    "memory_search",
    "coding",
    "vision",
    "device_control"
]

available_capabilities = [
    "planning",
    "memory_search",
    "coding",
    "reasoning",
    "provider_selection"
]

CapabilityMatchingEngine.show_match(
    required_capabilities,
    available_capabilities
)