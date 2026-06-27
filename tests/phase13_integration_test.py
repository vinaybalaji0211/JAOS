from brain.daemon_mode import DaemonMode
from brain.continuous_monitor import ContinuousMonitor
from brain.background_executive_observer import (
    BackgroundExecutiveObserver
)
from brain.maintenance_scheduler import (
    MaintenanceScheduler
)
from brain.memory_consolidation import (
    MemoryConsolidation
)
from brain.automatic_recovery import (
    AutomaticRecovery
)

print("\n=== PHASE 13 INTEGRATION TEST ===\n")

daemon = DaemonMode()
daemon.start()
daemon.show_status()

monitor = ContinuousMonitor()
monitor.show_status()

observer = BackgroundExecutiveObserver()
observer.show_observations()

scheduler = MaintenanceScheduler()
scheduler.schedule(
    "Memory Consolidation",
    "nightly",
    1
)
scheduler.show_tasks()

memory = MemoryConsolidation()
memory.add_short_term(
    "Strong JARVIS architecture",
    important=True
)
memory.consolidate()
memory.show_memory()

recovery = AutomaticRecovery()
recovery.report_failure(
    "Research Agent"
)
recovery.recover_all()

print("\n=== PHASE 13 COMPLETE ===")