from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.decision_model import DecisionModel
from executive_brain.registries.decision_registry import DecisionRegistry


registry = DecisionRegistry()

decision = DecisionModel(
    decision_type="USE_MEMORY",
    reason="Existing JAOS project detected.",
    confidence=0.98,
    status=LifecycleStatus.ACTIVE,
    related_intent_id="INT-001",
    related_context_snapshot_id="CTX-001"
)

decision.add_metadata(
    "memory_scope",
    "project"
)

registry.add(
    decision.decision_id,
    decision
)

print("Count:", registry.count())
print("Exists:", registry.exists(decision.decision_id))

stored = registry.get(decision.decision_id)
print("Retrieved:", stored.to_dict())

print("By Type:", len(registry.get_by_type("USE_MEMORY")))
print("Active:", len(registry.get_active_decisions()))
print("By Intent:", len(registry.get_by_intent("INT-001")))

registry.remove(decision.decision_id)

print("Final Count:", registry.count())