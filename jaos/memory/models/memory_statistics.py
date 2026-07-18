"""Memory statistics model for the JAOS Memory Platform."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, slots=True)
class MemoryStatistics:
    """Tracks access-related statistics for a memory record."""

    access_count: int = 0
    last_accessed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate statistics invariants."""

        if not isinstance(self.access_count, int):
            raise TypeError("access_count must be an integer")

        if self.access_count < 0:
            raise ValueError("access_count must not be negative")

        if (
            self.last_accessed_at is not None
            and not isinstance(self.last_accessed_at, datetime)
        ):
            raise TypeError(
                "last_accessed_at must be a datetime instance or None"
            )

        if self.access_count == 0 and self.last_accessed_at is not None:
            raise ValueError(
                "last_accessed_at must be None when access_count is zero"
            )

        if self.access_count > 0 and self.last_accessed_at is None:
            raise ValueError(
                "last_accessed_at is required when access_count is greater than zero"
            )

    def record_access(self, accessed_at: datetime) -> "MemoryStatistics":
        """Return updated immutable statistics for a new access."""

        if not isinstance(accessed_at, datetime):
            raise TypeError("accessed_at must be a datetime instance")

        return MemoryStatistics(
            access_count=self.access_count + 1,
            last_accessed_at=accessed_at,
        )