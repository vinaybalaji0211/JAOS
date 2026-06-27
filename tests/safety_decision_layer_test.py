from brain.safety_decision_layer import (
    SafetyDecisionLayer
)


print("\nSafe Task")

SafetyDecisionLayer.explain(
    risk_level="LOW",
    confidence=95,
    conflict_count=0,
    feasible=True,
    resources_ok=True
)


print("\nMedium Task")

SafetyDecisionLayer.explain(
    risk_level="MEDIUM",
    confidence=75,
    conflict_count=1,
    feasible=True,
    resources_ok=True
)


print("\nDangerous Task")

SafetyDecisionLayer.explain(
    risk_level="HIGH",
    confidence=50,
    conflict_count=2,
    feasible=True,
    resources_ok=False
)


print("\nBlocked Task")

SafetyDecisionLayer.explain(
    risk_level="BLOCKED",
    confidence=20,
    conflict_count=5,
    feasible=False,
    resources_ok=False
)