"""Conversation session storage contract for JAOS Intelligence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from jaos.intelligence.models import (
    ConversationSession,
    ConversationSessionState,
    IntelligenceIdentity,
)


class ConversationSessionStore(ABC):
    """
    Provider-independent storage boundary for conversation snapshots.

    Conversation sessions are runtime state, not permanent memory. Concrete
    implementations may use process memory, a database, or another approved
    runtime store without changing the Conversation Engine.
    """

    @abstractmethod
    def save_session(
        self,
        session: ConversationSession,
        *,
        expected_updated_at: datetime | None = None,
    ) -> ConversationSession:
        """
        Create or replace a session snapshot.

        When expected_updated_at is supplied, implementations must reject the
        write if the currently stored snapshot has a different update time.
        This provides optimistic-concurrency protection.
        """

        raise NotImplementedError

    @abstractmethod
    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Return the current immutable session snapshot when present."""

        raise NotImplementedError

    @abstractmethod
    def list_sessions(
        self,
        *,
        identity: IntelligenceIdentity | None = None,
        state: ConversationSessionState | None = None,
    ) -> tuple[ConversationSession, ...]:
        """Return matching session snapshots in deterministic order."""

        raise NotImplementedError

    @abstractmethod
    def delete_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """
        Remove and return ephemeral conversation state when present.

        This operation does not delete or modify Memory Platform records.
        """

        raise NotImplementedError

    @abstractmethod
    def contains(self, session_id: str) -> bool:
        """Return whether a session snapshot currently exists."""

        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of stored conversation sessions."""

        raise NotImplementedError