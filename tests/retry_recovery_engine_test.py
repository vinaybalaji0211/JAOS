from workflow.retry_recovery_engine import RetryRecoveryEngine

engine = RetryRecoveryEngine()

engine.register_failure(
    "Deploy Website",
    "GitHub Timeout"
)

engine.register_failure(
    "Generate Report",
    "OpenAI Quota Exceeded"
)

engine.show_failures()