from __future__ import annotations

from dataclasses import dataclass

from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType


@dataclass(frozen=True)
class MemoryFilter:
    """
    Optional filters used during memory search.
    """

    memory_type: MemoryType | None = None
    memory_scope: MemoryScope | None = None
    tags: tuple[str, ...] = ()
    minimum_importance: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.minimum_importance <= 1.0:
            raise ValueError(
                "minimum_importance must be between 0.0 and 1.0."
            )