from system_services.startup_manager import StartupManager
from system_services.configuration_manager import ConfigurationManager
from system_services.scheduler import Scheduler
from system_services.cache_manager import CacheManager
from system_services.cleanup_manager import CleanupManager
from system_services.update_manager import UpdateManager
from system_services.backup_manager import BackupManager

print("\n===== SYSTEM SERVICES TEST =====\n")

startup = StartupManager()
startup.register_service("JAOS Core")

config = ConfigurationManager()
config.set_value("theme", "dark")

scheduler = Scheduler()
scheduler.register_task(
    "Morning Briefing",
    "08:00 Daily"
)

cache = CacheManager()
cache.add_cache(
    "active_ai",
    "OpenAI"
)

cleanup = CleanupManager()
cleanup.register_cleanup(
    "Temporary Cache"
)

updates = UpdateManager()
updates.register_update(
    "JAOS Core Patch",
    "1.0.1-alpha"
)

backup = BackupManager()
backup.register_backup(
    "JAOS Backup",
    "C:/JARVIS/backups"
)

print("\n===== COMPONENT STATUS =====\n")

startup.show_services()
config.show_config()
scheduler.show_tasks()
cache.show_cache()
cleanup.show_tasks()
updates.show_updates()
backup.show_backups()

print("\n===== SYSTEM SERVICES COMPLETE =====")