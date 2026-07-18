"""Memory scope definitions for the JAOS Memory Platform."""

from enum import Enum


class MemoryScope(str, Enum):
    """Defines the visibility and ownership scope of a memory."""

    GLOBAL = "global"
    SYSTEM = "system"
    USER = "user"
    SESSION = "session"
    MISSION = "mission"