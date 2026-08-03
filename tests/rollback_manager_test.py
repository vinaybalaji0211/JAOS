from brain.rollback_manager import RollbackManager

manager = RollbackManager()

manager.create_checkpoint(
    "v1.0"
)

manager.create_checkpoint(
    "v1.1"
)

manager.rollback(
    "v1.0"
)

manager.show_history()