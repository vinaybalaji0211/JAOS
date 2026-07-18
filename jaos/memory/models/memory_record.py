"""Core memory record model for the JAOS Memory Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_lifecycle_state import MemoryLifecycleState
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_statistics import MemoryStatistics
from jaos.memory.models.memory_type import MemoryType


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    """Represents a structured memory stored by the Memory Platform."""

    content: str
    memory_type: MemoryType
    identity: MemoryIdentity
    source: str
    memory_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)
    importance: float = 0.5
    confidence: float = 1.0
    lifecycle_state: MemoryLifecycleState = MemoryLifecycleState.ACTIVE
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    statistics: MemoryStatistics = field(default_factory=MemoryStatistics)

    def __post_init__(self) -> None:
        """Validate and normalize memory record invariants."""

        if not isinstance(self.memory_id, str) or not self.memory_id.strip():
            raise ValueError("memory_id must be a non-empty string")

        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content must be a non-empty string")

        if not isinstance(self.memory_type, MemoryType):
            raise TypeError("memory_type must be an instance of MemoryType")

        if not isinstance(self.identity, MemoryIdentity):
            raise TypeError("identity must be an instance of MemoryIdentity")

        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("source must be a non-empty string")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if self.updated_at.tzinfo is None:
            raise ValueError("updated_at must be timezone-aware")

        if self.updated_at < self.created_at:
            raise ValueError("updated_at must not be earlier than created_at")

        if not isinstance(self.importance, (int, float)):
            raise TypeError("importance must be a number")

        if not 0.0 <= float(self.importance) <= 1.0:
            raise ValueError("importance must be between 0.0 and 1.0")

        if not isinstance(self.confidence, (int, float)):
            raise TypeError("confidence must be a number")

        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

        if not isinstance(self.lifecycle_state, MemoryLifecycleState):
            raise TypeError(
                "lifecycle_state must be an instance of MemoryLifecycleState"
            )

        if not isinstance(self.metadata, MemoryMetadata):
            raise TypeError("metadata must be an instance of MemoryMetadata")

        if not isinstance(self.statistics, MemoryStatistics):
            raise TypeError(
                "statistics must be an instance of MemoryStatistics"
            )

        object.__setattr__(self, "memory_id", self.memory_id.strip())
        object.__setattr__(self, "content", self.content.strip())
        object.__setattr__(self, "source", self.source.strip())
        object.__setattr__(self, "importance", float(self.importance))
        object.__setattr__(self, "confidence", float(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        """Return a storage-independent dictionary representation."""

        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "identity": {
                "scope": self.identity.scope.value,
                "identity_id": self.identity.identity_id,
            },
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "importance": self.importance,
            "confidence": self.confidence,
            "lifecycle_state": self.lifecycle_state.value,
            "metadata": self.metadata.to_dict(),
            "statistics": {
                "access_count": self.statistics.access_count,
                "last_accessed_at": (
                    self.statistics.last_accessed_at.isoformat()
                    if self.statistics.last_accessed_at is not None
                    else None
                ),
            },
        }