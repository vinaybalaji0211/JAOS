from brain.crash_recovery_system import CrashRecoverySystem

CrashRecoverySystem.save_checkpoint(
    last_state="ACTIVE",
    last_task="Phase 8 Self-Healing AI OS",
    last_goal="Build Independent 24/7 AI Operating System",
    crash_reason="Simulated crash test"
)

CrashRecoverySystem.show_checkpoint()