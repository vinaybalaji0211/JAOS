from brain.intrusion_detection_engine import (
    IntrusionDetectionEngine
)

engine = (
    IntrusionDetectionEngine()
)

engine.detect(
    "Multiple Failed Login Attempts",
    "HIGH"
)

engine.detect(
    "Unauthorized Upgrade Request",
    "CRITICAL"
)

engine.show_detections()