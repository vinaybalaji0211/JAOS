"""Conversation engine contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_bundle import (
    ContextBundle,
)
from jaos.intelligence.models.conversation_session import (
    ConversationSession,
)
from jaos.intelligence.models.conversation_turn import (
    ConversationTurn,
)
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.intelligence_result import (
    IntelligenceResult,
)


class ConversationEngine(IntelligenceComponent):
    """
    Defines the provider-independent contract for conversation
    orchestration.

    The Conversation Engine is responsible exclusively for managing
    conversation sessions, preserving conversational state, assembling
    contextual information, and coordinating conversational interaction
    with the Intelligence Platform.

    Implementations perform conversational activities such as:

    - Conversation session creation
    - Conversation state management
    - Context assembly
    - Turn processing
    - Session lifecycle management
    - Identity isolation
    - Conversation result synthesis

    The Conversation Engine represents the conversational coordination
    boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Preserve conversation session integrity
    - Maintain identity isolation
    - Remain free of observable side effects outside conversation state

    Implementations shall not:

    - Execute tools
    - Generate execution plans
    - Enforce security policies
    - Modify persistent memory outside conversation state
    - Construct provider-specific prompts
    - Perform provider routing
    - Execute external actions
    """

    @abstractmethod
    async def start_session(
        self,
        identity: IntelligenceIdentity,
        *,
        policy_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationSession:
        """
        Create and initialize a conversation session.

        Args:
            identity:
                The intelligence identity that owns the session.
            policy_name:
                Optional conversation policy.
            metadata:
                Optional session metadata.

        Returns:
            The initialized ConversationSession.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """
        Retrieve the current conversation session.

        Args:
            session_id:
                The unique conversation session identifier.

        Returns:
            The current ConversationSession if it exists;
            otherwise None.
        """

        raise NotImplementedError

    @abstractmethod
    async def process_turn(
        self,
        session_id: str,
        turn: ConversationTurn,
        context_bundle: ContextBundle,
    ) -> IntelligenceResult:
        """
        Process a single conversation turn.

        Implementations coordinate conversational processing while
        preserving session consistency and conversational context.

        Args:
            session_id:
                The active conversation session identifier.
            turn:
                The conversation turn to process.
            context_bundle:
                The contextual information available for this turn.

        Returns:
            A structured provider-independent IntelligenceResult.
        """

        raise NotImplementedError

    @abstractmethod
    async def close_session(
        self,
        session_id: str,
    ) -> ConversationSession:
        """
        Gracefully close a conversation session.

        Args:
            session_id:
                The conversation session identifier.

        Returns:
            The final immutable ConversationSession snapshot.
        """

        raise NotImplementedError
