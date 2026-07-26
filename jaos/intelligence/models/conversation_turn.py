"""Conversation turn model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.conversation_role import ConversationRole


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_identifier_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of identifiers."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{field_name} must contain only non-empty strings"
            )

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ConversationTurn:
    """Represents one structured turn in an intelligence conversation."""

    session_id: str
    role: ConversationRole
    content: str
    source: str = "conversation"
    turn_id: str = field(default_factory=lambda: str(uuid4()))
    structured_payload: dict[str, Any] = field(default_factory=dict)
    context_source_ids: tuple[str, ...] = ()
    tool_result_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize conversation turn invariants."""

        required_strings = {
            "turn_id": self.turn_id,
            "session_id": self.session_id,
            "content": self.content,
            "source": self.source,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(self.role, ConversationRole):
            raise TypeError(
                "role must be an instance of ConversationRole"
            )

        if not isinstance(self.structured_payload, dict):
            raise TypeError(
                "structured_payload must be a dictionary"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        object.__setattr__(self, "turn_id", self.turn_id.strip())
        object.__setattr__(self, "session_id", self.session_id.strip())
        object.__setattr__(self, "content", self.content.strip())
        object.__setattr__(self, "source", self.source.strip().lower())
        object.__setattr__(
            self,
            "structured_payload",
            dict(self.structured_payload),
        )
        object.__setattr__(
            self,
            "context_source_ids",
            _normalize_identifier_tuple(
                self.context_source_ids,
                "context_source_ids",
            ),
        )
        object.__setattr__(
            self,
            "tool_result_ids",
            _normalize_identifier_tuple(
                self.tool_result_ids,
                "tool_result_ids",
            ),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "turn_id": self.turn_id,
            "session_id": self.session_id,
            "role": self.role.value,
            "content": self.content,
            "source": self.source,
            "structured_payload": dict(self.structured_payload),
            "context_source_ids": list(self.context_source_ids),
            "tool_result_ids": list(self.tool_result_ids),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }