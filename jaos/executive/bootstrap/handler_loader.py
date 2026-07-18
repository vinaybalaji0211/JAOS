from jaos.executive.domains.filesystem.backup_file_handler import (
    BackupFileIntentHandler,
)
from jaos.executive.domains.filesystem.copy_file_handler import (
    CopyFileIntentHandler,
)
from jaos.executive.domains.filesystem.delete_file_handler import (
    DeleteFileIntentHandler,
)
from jaos.executive.domains.filesystem.move_file_handler import (
    MoveFileIntentHandler,
)
from jaos.executive.domains.filesystem.read_file_handler import (
    ReadFileIntentHandler,
)
from jaos.executive.domains.filesystem.rename_file_handler import (
    RenameFileIntentHandler,
)
from jaos.executive.domains.filesystem.search_file_handler import (
    SearchFileIntentHandler,
)
from jaos.executive.domains.filesystem.write_file_handler import (
    WriteFileIntentHandler,
)
from jaos.executive.intent_registry import ExecutiveIntentRegistry


def build_intent_registry() -> ExecutiveIntentRegistry:
    """
    Build and populate the Executive Intent Registry.

    All Executive capability domains register their handlers here.
    """

    registry = ExecutiveIntentRegistry()

    # Filesystem Domain
    registry.register(ReadFileIntentHandler())
    registry.register(WriteFileIntentHandler())
    registry.register(CopyFileIntentHandler())
    registry.register(MoveFileIntentHandler())
    registry.register(RenameFileIntentHandler())
    registry.register(DeleteFileIntentHandler())
    registry.register(SearchFileIntentHandler())
    registry.register(BackupFileIntentHandler())

    return registry