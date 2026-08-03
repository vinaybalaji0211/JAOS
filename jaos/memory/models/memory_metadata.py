"""Memory metadata model for the JAOS Memory Platform."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryMetadata:
    """Stores immutable auxiliary metadata for a memory record."""

    values: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize metadata."""

        if not isinstance(self.values, Mapping):
            raise TypeError("values must be a mapping")

        normalized: dict[str, Any] = {}

        for key, value in self.values.items():
            if not isinstance(key, str):
                raise TypeError("metadata keys must be strings")

            normalized_key = key.strip()

            if not normalized_key:
                raise ValueError("metadata keys must not be empty")

            normalized[normalized_key] = value

        object.__setattr__(self, "values", normalized)

    def get(self, key: str, default: Any = None) -> Any:
        """Return a metadata value by key."""

        return self.values.get(key, default)

    def to_dict(self) -> dict[str, Any]:
        """Return a shallow dictionary copy of the metadata."""

        return dict(self.values)