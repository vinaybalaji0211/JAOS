"""Memory lifecycle state definitions for the JAOS Memory Platform."""

from enum import Enum


class MemoryLifecycleState(str, Enum):
    """Represents the lifecycle state of a memory record."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    EXPIRED = "expired"
    DELETED = "deleted"