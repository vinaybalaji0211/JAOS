from brain.autonomous_maintenance_planner import AutonomousMaintenancePlanner
from brain.crash_recovery_system import CrashRecoverySystem
from brain.error_recovery_engine import ErrorRecoveryEngine
from brain.health_monitor import HealthMonitor
from brain.resource_recovery_engine import ResourceRecoveryEngine
from brain.self_repair_engine import SelfRepairEngine

print("\n=== PHASE 8 INTEGRATION TEST ===\n")

# Health Monitor
monitor = HealthMonitor()

monitor.update(
    "providers",
    "WARNING"
)

monitor.update(
    "voice_system",
    "FAILED"
)

monitor.show_health()

# Error Recovery
engine = ErrorRecoveryEngine()

engine.show_recovery(
    "VOICE_FAILURE"
)

# Crash Recovery
CrashRecoverySystem.save_checkpoint(

    last_state="ACTIVE",

    last_task="Self-Healing AI OS",

    last_goal="Build Independent AI Operating System",

    crash_reason="Simulated integration test"

)

CrashRecoverySystem.show_checkpoint()

# Self Repair
SelfRepairEngine.show_repair(
    "import_error"
)

# Resource Recovery
ResourceRecoveryEngine.show_recovery(
    "LOW_RAM"
)

# Autonomous Maintenance
AutonomousMaintenancePlanner.show_plan(

    health_status="CRITICAL",

    error_type="VOICE_FAILURE",

    resource_problem="LOW_RAM",

    crash_detected=True,

    repair_needed=True

)

print("\n=== PHASE 8 COMPLETE ===")