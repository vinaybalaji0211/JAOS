"""Conversation-history context source for JAOS Intelligence."""

from __future__ import annotations

from collections.abc import Callable
from threading import RLock

from jaos.intelligence.exceptions import (
    IntelligenceComponentStateError,
    IntelligenceContextError,
)
from jaos.intelligence.interfaces import IntelligenceContextSource
from jaos.intelligence.models import (
    ContextItem,
    ContextTrustLevel,
    ConversationRole,
    ConversationSession,
    ConversationTurn,
    IntelligenceContextType,
    IntelligenceRequest,
)

SessionResolver = Callable[[str], ConversationSession | None]


def _normalize_source_name(source_name: str) -> str:
    """Validate and normalize the source name."""

    if not isinstance(source_name, str):
        raise TypeError("source_name must be a string")

    normalized = source_name.strip().lower()

    if not normalized:
        raise ValueError("source_name must not be empty")

    return normalized


def _context_type_for_turn(
    turn: ConversationTurn,
) -> IntelligenceContextType:
    """Map a conversation role to an intelligence context type."""

    if turn.role is ConversationRole.MEMORY:
        return IntelligenceContextType.MEMORY

    if turn.role is ConversationRole.TOOL_RESULT:
        return IntelligenceContextType.TOOL_RESULT

    return IntelligenceContextType.CONVERSATION


def _trust_level_for_turn(
    turn: ConversationTurn,
) -> ContextTrustLevel:
    """Map a conversation role to a context trust level."""

    trust_levels = {
        ConversationRole.SYSTEM: ContextTrustLevel.TRUSTED_SYSTEM,
        ConversationRole.USER: ContextTrustLevel.USER_PROVIDED,
        ConversationRole.ASSISTANT: (
            ContextTrustLevel.TRUSTED_INTERNAL
        ),
        ConversationRole.MEMORY: (
            ContextTrustLevel.RETRIEVED_MEMORY
        ),
        ConversationRole.TOOL_RESULT: (
            ContextTrustLevel.TRUSTED_INTERNAL
        ),
    }

    return trust_levels[turn.role]


def _importance_for_turn(turn: ConversationTurn) -> float:
    """Return the deterministic importance score for a turn."""

    importance_scores = {
        ConversationRole.SYSTEM: 1.0,
        ConversationRole.USER: 0.85,
        ConversationRole.ASSISTANT: 0.75,
        ConversationRole.MEMORY: 0.8,
        ConversationRole.TOOL_RESULT: 0.7,
    }

    return importance_scores[turn.role]


def _confidence_for_turn(turn: ConversationTurn) -> float:
    """Return the deterministic confidence score for a turn."""

    confidence_scores = {
        ConversationRole.SYSTEM: 1.0,
        ConversationRole.USER: 0.8,
        ConversationRole.ASSISTANT: 0.85,
        ConversationRole.MEMORY: 0.75,
        ConversationRole.TOOL_RESULT: 0.9,
    }

    return confidence_scores[turn.role]


class ConversationHistoryContextSource(IntelligenceContextSource):
    """Adapts conversation-session history into context items."""

    def __init__(
        self,
        session_resolver: SessionResolver,
        *,
        source_name: str = "conversation-history",
        max_turns: int = 20,
    ) -> None:
        if not callable(session_resolver):
            raise TypeError("session_resolver must be callable")

        if isinstance(max_turns, bool) or not isinstance(
            max_turns,
            int,
        ):
            raise TypeError("max_turns must be an integer")

        if max_turns <= 0:
            raise ValueError("max_turns must be greater than zero")

        self._session_resolver = session_resolver
        self._source_name = _normalize_source_name(source_name)
        self._max_turns = max_turns
        self._ready = False
        self._lock = RLock()

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return f"context-source:{self._source_name}"

    @property
    def source_name(self) -> str:
        """Return the stable context-source name."""

        return self._source_name

    @property
    def is_ready(self) -> bool:
        """Return whether conversation context can be collected."""

        with self._lock:
            return self._ready

    def initialize(self) -> None:
        """Enable conversation-history collection."""

        with self._lock:
            self._ready = True

    def shutdown(self) -> None:
        """Disable conversation-history collection."""

        with self._lock:
            self._ready = False

    def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        """Collect approved history for the request session."""

        if not isinstance(request, IntelligenceRequest):
            raise TypeError(
                "request must be an instance of IntelligenceRequest"
            )

        if not self.is_ready:
            raise IntelligenceComponentStateError(
                "conversation history context source is not ready",
                request_id=request.request_id,
                component=self.component_name,
            )

        if request.session_id is None:
            return ()

        try:
            session = self._session_resolver(request.session_id)
        except Exception as exc:
            raise IntelligenceContextError(
                "conversation session resolution failed",
                request_id=request.request_id,
                details={
                    "session_id": request.session_id,
                    "error": str(exc),
                },
            ) from exc

        if session is None:
            return ()

        if not isinstance(session, ConversationSession):
            raise IntelligenceContextError(
                "conversation resolver returned an invalid session",
                request_id=request.request_id,
                details={"session_id": request.session_id},
            )

        if session.session_id != request.session_id:
            raise IntelligenceContextError(
                "resolved conversation session ID does not match request",
                request_id=request.request_id,
                details={
                    "requested_session_id": request.session_id,
                    "resolved_session_id": session.session_id,
                },
            )

        if session.identity != request.identity:
            raise IntelligenceContextError(
                "conversation session identity does not match request",
                request_id=request.request_id,
                details={"session_id": request.session_id},
            )

        selected_turns = session.turns[-self._max_turns :]
        turn_count = len(selected_turns)

        if turn_count == 0:
            return ()

        context_items: list[ContextItem] = []

        for index, turn in enumerate(selected_turns):
            recency_score = 0.6 + (
                0.4 * ((index + 1) / turn_count)
            )
            context_items.append(
                ContextItem(
                    item_id=f"conversation:{turn.turn_id}",
                    context_type=_context_type_for_turn(turn),
                    content=turn.content,
                    identity=session.identity,
                    source=self._source_name,
                    trust_level=_trust_level_for_turn(turn),
                    relevance=recency_score,
                    importance=_importance_for_turn(turn),
                    confidence=_confidence_for_turn(turn),
                    metadata={
                        "session_id": session.session_id,
                        "turn_id": turn.turn_id,
                        "conversation_role": turn.role.value,
                        "turn_source": turn.source,
                        "source_context_ids": list(
                            turn.context_source_ids
                        ),
                        "tool_result_ids": list(
                            turn.tool_result_ids
                        ),
                        "required_context": (
                            turn.role is ConversationRole.SYSTEM
                        ),
                    },
                    created_at=turn.created_at,
                )
            )

        return tuple(context_items)