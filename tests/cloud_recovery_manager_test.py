from brain.cloud_recovery_manager import CloudRecoveryManager

manager = (
    CloudRecoveryManager()
)

manager.recover(
    "KnowledgeGraph_Backup"
)

manager.recover(
    "EvolutionMemory_Backup"
)

manager.show_recovery_history()