"""Conversation session lifecycle management for JAOS Intelligence."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_policy_registry import (
    ConversationPolicyRegistry,
)
from jaos.intelligence.conversation.conversation_session_store import (
    ConversationSessionStore,
)
from jaos.intelligence.exceptions import (
    IntelligenceConversationError,
    IntelligencePermissionError,
)
from jaos.intelligence.models import (
    ConversationSession,
    ConversationSessionState,
    ConversationTurn,
    IntelligenceIdentity,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC time."""

    return datetime.now(timezone.utc)


class ConversationSessionManager:
    """Coordinates safe immutable conversation-session transitions."""

    def __init__(
        self,
        session_store: ConversationSessionStore,
        policy_registry: ConversationPolicyRegistry,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not isinstance(session_store, ConversationSessionStore):
            raise TypeError(
                "session_store must be a ConversationSessionStore"
            )

        if not isinstance(
            policy_registry,
            ConversationPolicyRegistry,
        ):
            raise TypeError(
                "policy_registry must be a ConversationPolicyRegistry"
            )

        resolved_clock = clock or _utc_now

        if not callable(resolved_clock):
            raise TypeError("clock must be callable")

        self._session_store = session_store
        self._policy_registry = policy_registry
        self._clock = resolved_clock

    def start_session(
        self,
        identity: IntelligenceIdentity,
        *,
        policy_name: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationSession:
        """Create and store a new active conversation session."""

        if not isinstance(identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an IntelligenceIdentity"
            )

        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a dictionary or None")

        policy = self._policy_registry.resolve_policy(policy_name)
        resolved_session_id = self._resolve_new_session_id(
            session_id
        )

        if self._session_store.contains(resolved_session_id):
            raise IntelligenceConversationError(
                "conversation session already exists",
                component="conversation_session_manager",
                details={"session_id": resolved_session_id},
            )

        now = self._get_time()
        session_metadata = dict(metadata or {})
        session_metadata["conversation_policy"] = (
            policy.policy_name
        )

        session = ConversationSession(
            identity=identity,
            session_id=resolved_session_id,
            state=ConversationSessionState.ACTIVE,
            max_history_turns=policy.max_history_turns,
            context_policy=policy.context_policy,
            metadata=session_metadata,
            created_at=now,
            updated_at=now,
        )

        return self._session_store.save_session(session)

    def get_session(
        self,
        session_id: str,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession | None:
        """Return a session when it exists and identity access is valid."""

        session = self._session_store.get_session(session_id)

        if session is not None:
            self._require_identity(session, identity)

        return session

    def get_required_session(
        self,
        session_id: str,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession:
        """Return an existing session or raise a structured error."""

        session = self.get_session(
            session_id,
            identity=identity,
        )

        if session is None:
            raise IntelligenceConversationError(
                "conversation session not found",
                component="conversation_session_manager",
                details={"session_id": str(session_id).strip()},
            )

        return session

    def append_turn(
        self,
        session_id: str,
        turn: ConversationTurn,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession:
        """Append one ordered, unique turn to an active session."""

        if not isinstance(turn, ConversationTurn):
            raise TypeError("turn must be a ConversationTurn")

        session = self.get_required_session(
            session_id,
            identity=identity,
        )
        self._require_state(
            session,
            ConversationSessionState.ACTIVE,
            operation="append_turn",
        )

        if turn.session_id != session.session_id:
            raise IntelligenceConversationError(
                "conversation turn session_id does not match session",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "turn_session_id": turn.session_id,
                    "turn_id": turn.turn_id,
                },
            )

        if turn.created_at < session.created_at:
            raise IntelligenceConversationError(
                "conversation turn predates its session",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "turn_id": turn.turn_id,
                },
            )

        if any(
            existing.turn_id == turn.turn_id
            for existing in session.turns
        ):
            raise IntelligenceConversationError(
                "conversation turn already exists",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "turn_id": turn.turn_id,
                },
            )

        if (
            session.turns
            and turn.created_at < session.turns[-1].created_at
        ):
            raise IntelligenceConversationError(
                "conversation turn is out of order",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "turn_id": turn.turn_id,
                },
            )

        turns = session.turns + (turn,)
        removed_turn_count = max(
            0,
            len(turns) - session.max_history_turns,
        )

        if removed_turn_count:
            turns = turns[removed_turn_count:]

        metadata = dict(session.metadata)

        if removed_turn_count:
            metadata["history_truncated_count"] = (
                int(metadata.get("history_truncated_count", 0))
                + removed_turn_count
            )

        updated = replace(
            session,
            turns=turns,
            metadata=metadata,
            updated_at=self._next_update_time(
                session,
                turn.created_at,
            ),
        )

        return self._session_store.save_session(
            updated,
            expected_updated_at=session.updated_at,
        )

    def interrupt_session(
        self,
        session_id: str,
        *,
        identity: IntelligenceIdentity | None = None,
        reason: str | None = None,
    ) -> ConversationSession:
        """Transition an active session into interrupted state."""

        session = self.get_required_session(
            session_id,
            identity=identity,
        )
        policy = self._resolve_session_policy(session)

        if not policy.allow_interruption:
            raise IntelligenceConversationError(
                "conversation policy does not allow interruption",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "policy_name": policy.policy_name,
                },
            )

        self._require_state(
            session,
            ConversationSessionState.ACTIVE,
            operation="interrupt_session",
        )

        normalized_reason = self._normalize_optional_reason(reason)
        updated_at = self._next_update_time(session)
        metadata = dict(session.metadata)
        metadata["interrupted_at"] = updated_at.isoformat()

        if normalized_reason is not None:
            metadata["interruption_reason"] = normalized_reason

        updated = replace(
            session,
            state=ConversationSessionState.INTERRUPTED,
            metadata=metadata,
            updated_at=updated_at,
        )

        return self._session_store.save_session(
            updated,
            expected_updated_at=session.updated_at,
        )

    def continue_session(
        self,
        session_id: str,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession:
        """Continue a policy-approved interrupted session."""

        session = self.get_required_session(
            session_id,
            identity=identity,
        )
        policy = self._resolve_session_policy(session)

        if not policy.allow_continuation:
            raise IntelligenceConversationError(
                "conversation policy does not allow continuation",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "policy_name": policy.policy_name,
                },
            )

        self._require_state(
            session,
            ConversationSessionState.INTERRUPTED,
            operation="continue_session",
        )

        updated_at = self._next_update_time(session)
        metadata = dict(session.metadata)
        metadata["continued_at"] = updated_at.isoformat()
        metadata["continuation_count"] = (
            int(metadata.get("continuation_count", 0)) + 1
        )

        updated = replace(
            session,
            state=ConversationSessionState.ACTIVE,
            metadata=metadata,
            updated_at=updated_at,
        )

        return self._session_store.save_session(
            updated,
            expected_updated_at=session.updated_at,
        )

    def close_session(
        self,
        session_id: str,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession:
        """Close an active or interrupted conversation session."""

        session = self.get_required_session(
            session_id,
            identity=identity,
        )

        if session.state is ConversationSessionState.CLOSED:
            return session

        if session.state is ConversationSessionState.FAILED:
            raise IntelligenceConversationError(
                "failed conversation session cannot be closed",
                component="conversation_session_manager",
                details={"session_id": session.session_id},
            )

        updated_at = self._next_update_time(session)
        metadata = dict(session.metadata)
        metadata["closed_at"] = updated_at.isoformat()

        updated = replace(
            session,
            state=ConversationSessionState.CLOSED,
            metadata=metadata,
            updated_at=updated_at,
        )

        return self._session_store.save_session(
            updated,
            expected_updated_at=session.updated_at,
        )

    def fail_session(
        self,
        session_id: str,
        reason: str,
        *,
        identity: IntelligenceIdentity | None = None,
    ) -> ConversationSession:
        """Transition a non-closed session into failed state."""

        session = self.get_required_session(
            session_id,
            identity=identity,
        )

        if session.state is ConversationSessionState.CLOSED:
            raise IntelligenceConversationError(
                "closed conversation session cannot be failed",
                component="conversation_session_manager",
                details={"session_id": session.session_id},
            )

        normalized_reason = self._normalize_required_reason(reason)
        updated_at = self._next_update_time(session)
        metadata = dict(session.metadata)
        metadata["failed_at"] = updated_at.isoformat()
        metadata["failure_reason"] = normalized_reason

        updated = replace(
            session,
            state=ConversationSessionState.FAILED,
            metadata=metadata,
            updated_at=updated_at,
        )

        return self._session_store.save_session(
            updated,
            expected_updated_at=session.updated_at,
        )

    def list_sessions(
        self,
        *,
        identity: IntelligenceIdentity | None = None,
        state: ConversationSessionState | None = None,
    ) -> tuple[ConversationSession, ...]:
        """Return filtered conversation snapshots."""

        return self._session_store.list_sessions(
            identity=identity,
            state=state,
        )

    def _resolve_session_policy(
        self,
        session: ConversationSession,
    ) -> ConversationPolicy:
        policy_name = session.metadata.get("conversation_policy")

        if policy_name is not None and not isinstance(
            policy_name,
            str,
        ):
            raise IntelligenceConversationError(
                "conversation session policy metadata is invalid",
                component="conversation_session_manager",
                details={"session_id": session.session_id},
            )

        return self._policy_registry.resolve_policy(policy_name)

    @staticmethod
    def _require_identity(
        session: ConversationSession,
        identity: IntelligenceIdentity | None,
    ) -> None:
        if identity is None:
            return

        if not isinstance(identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an IntelligenceIdentity or None"
            )

        if session.identity != identity:
            raise IntelligencePermissionError(
                "conversation session identity access denied",
                component="conversation_session_manager",
                details={"session_id": session.session_id},
            )

    @staticmethod
    def _require_state(
        session: ConversationSession,
        expected_state: ConversationSessionState,
        *,
        operation: str,
    ) -> None:
        if session.state is not expected_state:
            raise IntelligenceConversationError(
                "conversation session is in an invalid state",
                component="conversation_session_manager",
                details={
                    "session_id": session.session_id,
                    "operation": operation,
                    "expected_state": expected_state.value,
                    "actual_state": session.state.value,
                },
            )

    def _get_time(self) -> datetime:
        value = self._clock()

        if not isinstance(value, datetime):
            raise TypeError("clock must return a datetime")

        if value.tzinfo is None:
            raise ValueError(
                "clock must return a timezone-aware datetime"
            )

        return value

    def _next_update_time(
        self,
        session: ConversationSession,
        candidate: datetime | None = None,
    ) -> datetime:
        current_time = self._get_time()
        next_time = max(
            value
            for value in (
                current_time,
                candidate,
                session.updated_at,
            )
            if value is not None
        )

        if next_time <= session.updated_at:
            next_time = (
                session.updated_at
                + timedelta(microseconds=1)
            )

        return next_time

    @staticmethod
    def _resolve_new_session_id(
        session_id: str | None,
    ) -> str:
        if session_id is None:
            return str(uuid4())

        if not isinstance(session_id, str):
            raise TypeError("session_id must be a string or None")

        normalized = session_id.strip()

        if not normalized:
            raise ValueError(
                "session_id must not be empty when provided"
            )

        return normalized

    @staticmethod
    def _normalize_optional_reason(
        reason: str | None,
    ) -> str | None:
        if reason is None:
            return None

        return ConversationSessionManager._normalize_required_reason(
            reason
        )

    @staticmethod
    def _normalize_required_reason(reason: str) -> str:
        if not isinstance(reason, str):
            raise TypeError("reason must be a string")

        normalized = reason.strip()

        if not normalized:
            raise ValueError("reason must not be empty")

        return normalized