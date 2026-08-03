from brain.resource_recovery_engine import ResourceRecoveryEngine

ResourceRecoveryEngine.show_recovery(
    "LOW_RAM"
)

ResourceRecoveryEngine.show_recovery(
    "GPU_OOM"
)

ResourceRecoveryEngine.show_recovery(
    "DISK_FULL"
)