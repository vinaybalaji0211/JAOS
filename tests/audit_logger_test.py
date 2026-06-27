from security.audit_logger import AuditLogger

audit = AuditLogger()

audit.log_action(
    "Vinay",
    "OPEN_VSCODE",
    "SUCCESS"
)

audit.log_action(
    "Admin",
    "DELETE_TEMP_FILES",
    "SUCCESS"
)

audit.show_records()