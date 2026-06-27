from system_services.scheduler import Scheduler

scheduler = Scheduler()

scheduler.register_task(
    "Morning Briefing",
    "08:00 Daily"
)

scheduler.register_task(
    "Automatic Backup",
    "22:00 Daily"
)

scheduler.show_tasks()