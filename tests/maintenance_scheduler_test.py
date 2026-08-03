from brain.maintenance_scheduler import MaintenanceScheduler

scheduler = MaintenanceScheduler()

scheduler.schedule(
    "Health Check",
    "hourly",
    priority=1
)

scheduler.schedule(
    "Memory Consolidation",
    "nightly",
    priority=2
)

scheduler.schedule(
    "Backup Recovery Vault",
    "daily",
    priority=3
)

scheduler.show_tasks()

scheduler.complete(
    "Health Check"
)

scheduler.show_tasks()