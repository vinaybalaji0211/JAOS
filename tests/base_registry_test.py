from executive_brain.registries.base_registry import BaseRegistry

registry = BaseRegistry()

registry.add(
    "ITEM-001",
    {
        "name": "Test Item"
    }
)

print("Count:", registry.count())
print("Exists:", registry.exists("ITEM-001"))
print("Get:", registry.get("ITEM-001"))

registry.update(
    "ITEM-001",
    {
        "name": "Updated Item"
    }
)

print("Updated:", registry.get("ITEM-001"))

removed = registry.remove("ITEM-001")

print("Removed:", removed)
print("Final Count:", registry.count())