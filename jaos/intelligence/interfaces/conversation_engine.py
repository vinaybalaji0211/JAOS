"""Conversation engine contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod
from typing import Any

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_bundle import ContextBundle
from jaos.intelligence.models.conversation_session import ConversationSession
from jaos.intelligence.models.conversation_turn import ConversationTurn
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.intelligence_result import IntelligenceResult


class ConversationEngine(IntelligenceComponent):
    """
    Defines stateful conversation processing operations.

    Implementations manage immutable conversation-session snapshots,
    preserve identity isolation, assemble contextual turn history, and
    return structured intelligence results.
    """

    @abstractmethod
    def start_session(
        self,
        identity: IntelligenceIdentity,
        *,
        policy_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationSession:
        """Create and return a policy-controlled conversation session."""

        raise NotImplementedError

    @abstractmethod
    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Return the current session snapshot when it exists."""

        raise NotImplementedError

    @abstractmethod
    def process_turn(
        self,
        session_id: str,
        turn: ConversationTurn,
        context_bundle: ContextBundle,
    ) -> IntelligenceResult:
        """Process one conversation turn and return intelligence output."""

        raise NotImplementedError

    @abstractmethod
    def close_session(
        self,
        session_id: str,
    ) -> ConversationSession:
        """Close a conversation session and return its final snapshot."""

        raise NotImplementedError