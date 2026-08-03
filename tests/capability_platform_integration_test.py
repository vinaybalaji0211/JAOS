from brain.capability_awareness_engine import CapabilityAwarenessEngine
from brain.feature_request_intelligence import FeatureRequestIntelligence
from brain.roadmap_recommendation_engine import RoadmapRecommendationEngine
from brain.unsupported_request_logger import UnsupportedRequestLogger
from brain.version_capability_registry import VersionCapabilityRegistry

print("\n===== CAPABILITY PLATFORM TEST =====\n")

# Capability Awareness
capability = CapabilityAwarenessEngine()

capability.register(
    "GitHub Integration",
    "JAOS v1 Alpha"
)

capability.register(
    "Robot Control",
    "JAOS v7"
)

print(capability.check("Robot Control"))

# Version Registry
registry = VersionCapabilityRegistry()

registry.register_feature(
    "JAOS v1 Alpha",
    "GitHub Integration"
)

registry.register_feature(
    "JAOS v7",
    "Robot Control"
)

registry.show_version(
    "JAOS v1 Alpha"
)

# Unsupported Logger
unsupported = UnsupportedRequestLogger()

unsupported.log_request(
    "Robot Control",
    "JAOS v7"
)

unsupported.show_requests()

# Feature Intelligence
feature = FeatureRequestIntelligence()

feature.add_request("Mobile Companion")
feature.add_request("Mobile Companion")
feature.add_request("Robot Control")

feature.show_statistics()

# Roadmap Recommendation
roadmap = RoadmapRecommendationEngine()

roadmap.recommend(
    "Mobile Companion",
    "JAOS v3",
    "JAOS v2",
    "High user demand."
)

roadmap.show_recommendations()

print("\n===== CAPABILITY PLATFORM COMPLETE =====")