from security.identity_manager import IdentityManager
from security.authentication_manager import AuthenticationManager
from security.authorization_manager import AuthorizationManager
from security.permission_manager import PermissionManager
from security.audit_logger import AuditLogger
from security.security_monitor import SecurityMonitor

print("\n===== SECURITY PLATFORM TEST =====\n")

identity = IdentityManager()
identity.register_identity("Vinay")

authentication = AuthenticationManager()
authentication.register_method(
    "Vinay",
    "Password"
)

authorization = AuthorizationManager()
authorization.register_role(
    "Vinay",
    "USER"
)

permissions = PermissionManager()
permissions.grant_permission(
    "Vinay",
    "OPEN_VSCODE"
)

audit = AuditLogger()
audit.log_action(
    "Vinay",
    "OPEN_VSCODE",
    "SUCCESS"
)

monitor = SecurityMonitor()
monitor.record_event(
    "LOW",
    "VS Code opened."
)

print("\n===== COMPONENT STATUS =====\n")

identity.show_identities()
authentication.show_methods()
authorization.show_roles()
permissions.show_permissions()
audit.show_records()
monitor.show_events()

print("\n===== SECURITY PLATFORM COMPLETE =====")