"""
Canonical vocabulary for Executive Intent parsing.
"""

from collections.abc import Iterable

READ_FILE_ALIASES = ("read", "open", "show", "display")
WRITE_FILE_ALIASES = ("write", "create", "save")
COPY_FILE_ALIASES = ("copy", "duplicate", "clone")
MOVE_FILE_ALIASES = ("move", "relocate")
RENAME_FILE_ALIASES = ("rename", "rename_file", "change_name")
DELETE_FILE_ALIASES = ("delete", "remove", "erase")
SEARCH_FILE_ALIASES = ("search", "find", "locate")
BACKUP_FILE_ALIASES = ("backup", "back_up")


def matches(command: str, aliases: Iterable[str]) -> bool:
    normalized = command.strip().lower()

    return any(
        normalized.startswith(f"{alias} ")
        for alias in aliases
    )