from security.permission_manager import PermissionManager

manager = PermissionManager()

manager.grant_permission(
    "Vinay",
    "OPEN_VSCODE"
)

manager.grant_permission(
    "Vinay",
    "READ_FILES"
)

manager.grant_permission(
    "Admin",
    "DELETE_SYSTEM_FILES"
)

manager.show_permissions()

print()

print(
    "Vinay OPEN_VSCODE:",
    manager.has_permission(
        "Vinay",
        "OPEN_VSCODE"
    )
)

print(
    "Vinay DELETE_SYSTEM_FILES:",
    manager.has_permission(
        "Vinay",
        "DELETE_SYSTEM_FILES"
    )
)