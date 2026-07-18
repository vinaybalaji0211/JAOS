"""Memory query model for the JAOS Memory Platform."""

from dataclasses import dataclass
from typing import Optional

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    """Represents criteria used to retrieve memory records."""

    query_text: str
    memory_types: tuple[MemoryType, ...] = ()
    scope: Optional[MemoryScope] = None
    identity: Optional[MemoryIdentity] = None
    minimum_importance: float = 0.0
    minimum_confidence: float = 0.0
    max_results: int = 10

    def __post_init__(self) -> None:
        """Validate and normalize query criteria."""

        if not isinstance(self.query_text, str) or not self.query_text.strip():
            raise ValueError("query_text must be a non-empty string")

        if not isinstance(self.memory_types, tuple):
            raise TypeError("memory_types must be a tuple")

        for memory_type in self.memory_types:
            if not isinstance(memory_type, MemoryType):
                raise TypeError(
                    "every item in memory_types must be a MemoryType"
                )

        if self.scope is not None and not isinstance(self.scope, MemoryScope):
            raise TypeError("scope must be a MemoryScope instance or None")

        if (
            self.identity is not None
            and not isinstance(self.identity, MemoryIdentity)
        ):
            raise TypeError(
                "identity must be a MemoryIdentity instance or None"
            )

        if not isinstance(self.minimum_importance, (int, float)):
            raise TypeError("minimum_importance must be a number")

        if not 0.0 <= float(self.minimum_importance) <= 1.0:
            raise ValueError(
                "minimum_importance must be between 0.0 and 1.0"
            )

        if not isinstance(self.minimum_confidence, (int, float)):
            raise TypeError("minimum_confidence must be a number")

        if not 0.0 <= float(self.minimum_confidence) <= 1.0:
            raise ValueError(
                "minimum_confidence must be between 0.0 and 1.0"
            )

        if not isinstance(self.max_results, int):
            raise TypeError("max_results must be an integer")

        if self.max_results <= 0:
            raise ValueError("max_results must be greater than zero")

        object.__setattr__(self, "query_text", self.query_text.strip())
        object.__setattr__(
            self,
            "minimum_importance",
            float(self.minimum_importance),
        )
        object.__setattr__(
            self,
            "minimum_confidence",
            float(self.minimum_confidence),
        )