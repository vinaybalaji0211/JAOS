from system_services.backup_manager import BackupManager

manager = BackupManager()

manager.register_backup(
    "JAOS Code Backup",
    "C:/JARVIS/backups"
)

manager.register_backup(
    "Memory Backup",
    "C:/JARVIS/backups/memory",
    "PENDING"
)

manager.show_backups()