from brain.automatic_recovery import AutomaticRecovery

recovery = AutomaticRecovery()

recovery.report_failure(
    "Plugin Manager"
)

recovery.report_failure(
    "Research Agent"
)

recovery.recover_all()

recovery.recover_all()