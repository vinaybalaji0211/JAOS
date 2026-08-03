from brain.security_audit_system import SecurityAuditSystem

audit = SecurityAuditSystem()

audit.log_event(
    "RUN_DIAGNOSTICS",
    "ALLOW",
    "SUCCESS"
)

audit.log_event(
    "INSTALL_PACKAGE",
    "REQUIRE_APPROVAL",
    "WAITING"
)

audit.log_event(
    "DELETE_FILE",
    "BLOCK",
    "DENIED"
)

audit.show_logs()