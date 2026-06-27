from brain.feature_request_intelligence import (
    FeatureRequestIntelligence
)

engine = FeatureRequestIntelligence()

engine.add_request("Mobile Companion")
engine.add_request("Robot Control")
engine.add_request("Mobile Companion")
engine.add_request("Smart Home")
engine.add_request("Mobile Companion")

engine.show_statistics()

top = engine.most_requested()

print(
    "\nMost Requested:",
    top
)