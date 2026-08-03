from brain.cloud_backup_engine import CloudBackupEngine

engine = CloudBackupEngine()

engine.create_backup(
    "KnowledgeGraph_Backup"
)

engine.create_backup(
    "EvolutionMemory_Backup"
)

engine.verify_backup(
    "KnowledgeGraph_Backup"
)

engine.show_backups()