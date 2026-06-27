from brain.error_recovery_engine import (
    ErrorRecoveryEngine
)

engine = ErrorRecoveryEngine()

engine.show_recovery(
    "GPU_OOM"
)

engine.show_recovery(
    "VOICE_FAILURE"
)

engine.show_recovery(
    "UNKNOWN_ERROR"
)