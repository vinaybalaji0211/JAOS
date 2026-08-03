from engineering.module_registry import ModuleRegistry

registry = ModuleRegistry()

registry.register_module(
    "Memory Manager",
    "Memory",
    "v1 Alpha",
    description="Handles long-term memory."
)

registry.register_module(
    "Permission Manager",
    "Security",
    "v1 Alpha",
    description="Controls permissions."
)

registry.show_modules()