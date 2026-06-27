from brain.tool_permission_manager import (
    ToolPermissionManager
)

manager = (
    ToolPermissionManager()
)

manager.register_tool(
    "WebSearch",
    False
)

manager.register_tool(
    "DeleteFile",
    True
)

manager.register_tool(
    "SendEmail",
    True
)

manager.show_permissions()

print(
    manager.requires_approval(
        "DeleteFile"
    )
)

print(
    manager.requires_approval(
        "WebSearch"
    )
)