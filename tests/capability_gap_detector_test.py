from brain.capability_gap_detector import (
    CapabilityGapDetector
)


missing_capabilities = [
    "vision",
    "device_control",
    "web_search",
    "object_detection"
]

CapabilityGapDetector.show_gaps(
    missing_capabilities
)