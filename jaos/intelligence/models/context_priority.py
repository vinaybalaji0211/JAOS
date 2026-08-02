"""Priority levels for intelligence context."""

from enum import IntEnum


class ContextPriority(IntEnum):
    """Defines context importance."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4