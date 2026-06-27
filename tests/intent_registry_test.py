from executive_brain.common.enums import Priority, LifecycleStatus
from executive_brain.models.intent_model import IntentModel
from executive_brain.registries.intent_registry import IntentRegistry


registry = IntentRegistry()

intent = IntentModel(
    intent_type="OPEN_APPLICATION",
    source="USER",
    priority=Priority.HIGH,
    confidence=0.98,
    status=LifecycleStatus.ACTIVE
)

intent.add_metadata(
    "application",
    "VS Code"
)

registry.add(
    intent.intent_id,
    intent
)

print("Count:", registry.count())
print("Exists:", registry.exists(intent.intent_id))

stored = registry.get(intent.intent_id)
print("Retrieved:", stored.to_dict())

print("By Type:", len(registry.get_by_type("OPEN_APPLICATION")))
print("Active:", len(registry.get_active_intents()))

registry.remove(intent.intent_id)

print("Final Count:", registry.count())