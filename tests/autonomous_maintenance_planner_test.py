from brain.autonomous_maintenance_planner import AutonomousMaintenancePlanner

AutonomousMaintenancePlanner.show_plan(
    health_status="CRITICAL",
    error_type="VOICE_FAILURE",
    resource_problem="LOW_RAM",
    crash_detected=True,
    repair_needed=True
)

AutonomousMaintenancePlanner.show_plan(
    health_status="GOOD"
)