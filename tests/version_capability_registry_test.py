from brain.version_capability_registry import (
    VersionCapabilityRegistry
)

registry = (
    VersionCapabilityRegistry()
)

registry.register_feature(
    "JAOS v1 Alpha",
    "Executive Brain"
)

registry.register_feature(
    "JAOS v1 Alpha",
    "Reasoning Engine"
)

registry.register_feature(
    "JAOS v2",
    "Workflow Automation"
)

registry.register_feature(
    "JAOS v7",
    "Robot Control"
)

registry.show_version(
    "JAOS v1 Alpha"
)

registry.show_version(
    "JAOS v7"
)