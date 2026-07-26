"""Conversation session model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.conversation_session_state import (
    ConversationSessionState,
)
from jaos.intelligence.models.conversation_turn import ConversationTurn
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class ConversationSession:
    """Represents a structured multi-turn intelligence conversation."""

    identity: IntelligenceIdentity
    session_id: str = field(default_factory=lambda: str(uuid4()))
    state: ConversationSessionState = ConversationSessionState.ACTIVE
    turns: tuple[ConversationTurn, ...] = ()
    max_history_turns: int = 100
    context_policy: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize conversation session invariants."""

        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("session_id must be a non-empty string")

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an instance of IntelligenceIdentity"
            )

        if not isinstance(self.state, ConversationSessionState):
            raise TypeError(
                "state must be an instance of ConversationSessionState"
            )

        try:
            turns = tuple(self.turns)
        except TypeError as exc:
            raise TypeError(
                "turns must be a collection of ConversationTurn instances"
            ) from exc

        for turn in turns:
            if not isinstance(turn, ConversationTurn):
                raise TypeError(
                    "turns must contain only ConversationTurn instances"
                )

            if turn.session_id.strip() != self.session_id.strip():
                raise ValueError(
                    "every conversation turn must match session_id"
                )

        for previous, current in zip(turns, turns[1:]):
            if current.created_at < previous.created_at:
                raise ValueError(
                    "conversation turns must be ordered by created_at"
                )

        if isinstance(self.max_history_turns, bool) or not isinstance(
            self.max_history_turns,
            int,
        ):
            raise TypeError("max_history_turns must be an integer")

        if self.max_history_turns <= 0:
            raise ValueError(
                "max_history_turns must be greater than zero"
            )

        if len(turns) > self.max_history_turns:
            raise ValueError(
                "conversation turns exceed max_history_turns"
            )

        if self.context_policy is not None and not isinstance(
            self.context_policy,
            str,
        ):
            raise TypeError("context_policy must be a string or None")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if self.updated_at.tzinfo is None:
            raise ValueError("updated_at must be timezone-aware")

        if self.updated_at < self.created_at:
            raise ValueError(
                "updated_at must not be earlier than created_at"
            )

        context_policy = (
            self.context_policy.strip().lower()
            if self.context_policy is not None
            else None
        )

        object.__setattr__(self, "session_id", self.session_id.strip())
        object.__setattr__(self, "turns", turns)
        object.__setattr__(
            self,
            "context_policy",
            context_policy or None,
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "session_id": self.session_id,
            "identity": self.identity.to_dict(),
            "state": self.state.value,
            "turns": [turn.to_dict() for turn in self.turns],
            "max_history_turns": self.max_history_turns,
            "context_policy": self.context_policy,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }