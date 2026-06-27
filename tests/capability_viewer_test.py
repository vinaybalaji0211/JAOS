from dashboard.capability_viewer import (
    CapabilityViewer
)

viewer = CapabilityViewer()

viewer.register_capability(
    "Open VS Code",
    True,
    "v1 Alpha"
)

viewer.register_capability(
    "Autonomous Self-Improvement",
    False,
    "v2.0"
)

viewer.show_capabilities()