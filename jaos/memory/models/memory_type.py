"""Memory type definitions for the JAOS Memory Platform."""

from enum import Enum


class MemoryType(str, Enum):
    """Classifies a memory according to its purpose and persistence."""

    WORKING = "working"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"