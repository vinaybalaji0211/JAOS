"""Thread-safe in-memory conversation session storage."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from threading import RLock

from jaos.intelligence.conversation.conversation_session_store import (
    ConversationSessionStore,
)
from jaos.intelligence.exceptions import IntelligenceConversationError
from jaos.intelligence.models import (
    ConversationSession,
    ConversationSessionState,
    IntelligenceIdentity,
)


def _normalize_session_id(session_id: str) -> str:
    """Validate and normalize a conversation session identifier."""

    if not isinstance(session_id, str):
        raise TypeError("session_id must be a string")

    normalized = session_id.strip()

    if not normalized:
        raise ValueError("session_id must not be empty")

    return normalized


def _validate_expected_updated_at(
    expected_updated_at: datetime | None,
) -> datetime | None:
    """Validate an optional optimistic-concurrency timestamp."""

    if expected_updated_at is None:
        return None

    if not isinstance(expected_updated_at, datetime):
        raise TypeError(
            "expected_updated_at must be a datetime or None"
        )

    if expected_updated_at.tzinfo is None:
        raise ValueError(
            "expected_updated_at must be timezone-aware"
        )

    return expected_updated_at


class InMemoryConversationSessionStore(ConversationSessionStore):
    """
    Stores isolated conversation snapshots in process memory.

    This implementation is intended for local runtime operation, tests, and
    development. It does not create or modify permanent Memory Platform data.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, ConversationSession] = {}
        self._lock = RLock()

    def save_session(
        self,
        session: ConversationSession,
        *,
        expected_updated_at: datetime | None = None,
    ) -> ConversationSession:
        """Store a defensive copy of a conversation snapshot."""

        if not isinstance(session, ConversationSession):
            raise TypeError(
                "session must be a ConversationSession"
            )

        normalized_expected = _validate_expected_updated_at(
            expected_updated_at
        )

        with self._lock:
            current = self._sessions.get(session.session_id)

            if normalized_expected is not None:
                if current is None:
                    raise IntelligenceConversationError(
                        "conversation session concurrency check failed",
                        component="conversation_session_store",
                        details={
                            "session_id": session.session_id,
                            "reason": "session_not_found",
                            "expected_updated_at": (
                                normalized_expected.isoformat()
                            ),
                        },
                    )

                if current.updated_at != normalized_expected:
                    raise IntelligenceConversationError(
                        "conversation session concurrency check failed",
                        component="conversation_session_store",
                        details={
                            "session_id": session.session_id,
                            "reason": "stale_snapshot",
                            "expected_updated_at": (
                                normalized_expected.isoformat()
                            ),
                            "actual_updated_at": (
                                current.updated_at.isoformat()
                            ),
                        },
                    )

            stored = deepcopy(session)
            self._sessions[session.session_id] = stored

            return deepcopy(stored)

    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Return an isolated copy of the current session snapshot."""

        normalized_id = _normalize_session_id(session_id)

        with self._lock:
            session = self._sessions.get(normalized_id)

            return (
                deepcopy(session)
                if session is not None
                else None
            )

    def list_sessions(
        self,
        *,
        identity: IntelligenceIdentity | None = None,
        state: ConversationSessionState | None = None,
    ) -> tuple[ConversationSession, ...]:
        """Return matching snapshots in deterministic creation order."""

        if identity is not None and not isinstance(
            identity,
            IntelligenceIdentity,
        ):
            raise TypeError(
                "identity must be an IntelligenceIdentity or None"
            )

        if state is not None and not isinstance(
            state,
            ConversationSessionState,
        ):
            raise TypeError(
                "state must be a ConversationSessionState or None"
            )

        with self._lock:
            sessions = tuple(self._sessions.values())

        filtered = (
            session
            for session in sessions
            if (
                identity is None
                or session.identity == identity
            )
            and (
                state is None
                or session.state is state
            )
        )

        ordered = sorted(
            filtered,
            key=lambda session: (
                session.created_at,
                session.session_id,
            ),
        )

        return tuple(
            deepcopy(session)
            for session in ordered
        )

    def delete_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Remove and return an isolated session snapshot."""

        normalized_id = _normalize_session_id(session_id)

        with self._lock:
            session = self._sessions.pop(normalized_id, None)

            return (
                deepcopy(session)
                if session is not None
                else None
            )

    def contains(self, session_id: str) -> bool:
        """Return whether a session exists."""

        normalized_id = _normalize_session_id(session_id)

        with self._lock:
            return normalized_id in self._sessions

    def __len__(self) -> int:
        """Return the current number of stored sessions."""

        with self._lock:
            return len(self._sessions)