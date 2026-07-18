from __future__ import annotations

from dataclasses import dataclass, field

from jaos.memory.models.memory_record import MemoryRecord


@dataclass(frozen=True)
class MemoryResult:
    """
    Result returned from memory search operations.
    """

    records: list[MemoryRecord] = field(default_factory=list)
    total_matches: int = 0
    query_time_ms: float = 0.0

    def __post_init__(self) -> None:
        if self.total_matches < 0:
            raise ValueError("total_matches cannot be negative.")

        if self.query_time_ms < 0:
            raise ValueError("query_time_ms cannot be negative.")