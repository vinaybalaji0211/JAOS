from core.permission_system import PermissionSystem

permissions = PermissionSystem()

permissions.show_permissions()

print("\nCheck delete_file:")

print(
    permissions.is_allowed("delete_file")
)

print("\nCheck read_file:")

print(
    permissions.is_allowed("read_file")
)
