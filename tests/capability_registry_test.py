from core.capability_registry import CapabilityRegistry

registry = CapabilityRegistry()

registry.register_capability(
    "File Manager",
    "read_file"
)

registry.register_capability(
    "File Manager",
    "write_file"
)

registry.register_capability(
    "Permission System",
    "check_permission"
)

registry.register_capability(
    "Agent Manager",
    "register_agent"
)

registry.show_capabilities()