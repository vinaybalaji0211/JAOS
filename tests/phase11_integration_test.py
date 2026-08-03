from brain.capability_restrictions import CapabilityRestrictions
from brain.human_approval_layer import HumanApprovalLayer
from brain.permission_firewall import PermissionFirewall
from brain.safe_execution_sandbox import SafeExecutionSandbox
from brain.secrets_manager import SecretsManager
from brain.security_audit_system import SecurityAuditSystem

print("\n=== PHASE 11 INTEGRATION TEST ===\n")

# Firewall
PermissionFirewall.show_decision(
    "INSTALL_PACKAGE"
)

# Approval
HumanApprovalLayer.show_request(
    "INSTALL_PACKAGE",
    "REQUIRE_APPROVAL"
)

# Sandbox
SafeExecutionSandbox.show_level(
    "INSTALL_PACKAGE"
)

# Secrets
manager = SecretsManager()

manager.store(
    "OPENAI_API_KEY",
    "secret_key"
)

manager.show_keys()

# Audit
audit = SecurityAuditSystem()

audit.log_event(
    "INSTALL_PACKAGE",
    "REQUIRE_APPROVAL",
    "WAITING"
)

audit.show_logs()

# Capability
CapabilityRestrictions.show_level(
    "INSTALL_PACKAGE"
)

print("\n=== PHASE 11 COMPLETE ===")