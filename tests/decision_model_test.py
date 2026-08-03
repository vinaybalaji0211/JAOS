from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.decision_model import DecisionModel

decision = DecisionModel(
    decision_type="USE_MEMORY",
    reason="Existing JAOS project detected.",
    confidence=0.98,
    related_intent_id="INT-001",
    related_context_snapshot_id="CTX-001"
)

decision.update_status(LifecycleStatus.ACTIVE)

decision.add_metadata(
    "memory_scope",
    "project"
)

print()
print(decision.to_dict())