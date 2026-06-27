from kernel.kernel_permission_gateway import (
    KernelPermissionGateway
)

gateway = KernelPermissionGateway()

gateway.grant_permission(
    "OPEN_VSCODE"
)

gateway.grant_permission(
    "DELETE_TEMP_FILES"
)

gateway.revoke_permission(
    "DELETE_TEMP_FILES"
)

gateway.show_permissions()

print()

print(
    gateway.is_allowed(
        "OPEN_VSCODE"
    )
)