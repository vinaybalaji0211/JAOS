"""Tests for the conversation-history context source."""

from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ContextTrustLevel,
    ConversationRole,
    ConversationSession,
    ConversationTurn,
    IntelligenceComponentStateError,
    IntelligenceContextError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ConversationHistoryContextSource,
    DefaultIntelligenceContextManager,
)


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_session(
    *,
    session_id: str = "session-001",
    identity: IntelligenceIdentity | None = None,
    roles: tuple[ConversationRole, ...] = (
        ConversationRole.SYSTEM,
        ConversationRole.USER,
        ConversationRole.ASSISTANT,
    ),
) -> ConversationSession:
    resolved_identity = identity or create_identity()
    now = datetime.now(timezone.utc)
    turns = tuple(
        ConversationTurn(
            session_id=session_id,
            role=role,
            content=f"{role.value} content",
            source="test",
            context_source_ids=(f"source-{index}",),
            tool_result_ids=(
                (f"tool-{index}",)
                if role is ConversationRole.TOOL_RESULT
                else ()
            ),
            created_at=now - timedelta(
                minutes=len(roles) - index
            ),
        )
        for index, role in enumerate(roles)
    )

    return ConversationSession(
        identity=resolved_identity,
        session_id=session_id,
        turns=turns,
        created_at=now - timedelta(minutes=len(roles) + 1),
        updated_at=now,
    )


def create_request(
    *,
    session_id: str | None = "session-001",
    identity: IntelligenceIdentity | None = None,
) -> IntelligenceRequest:
    return IntelligenceRequest(
        objective="Use conversation history",
        request_type=IntelligenceRequestType.CONTEXT,
        identity=identity or create_identity(),
        session_id=session_id,
    )


def test_conversation_source_lifecycle() -> None:
    source = ConversationHistoryContextSource(
        lambda session_id: None
    )

    assert source.component_name == (
        "context-source:conversation-history"
    )
    assert source.source_name == "conversation-history"
    assert source.is_ready is False

    source.initialize()

    assert source.is_ready is True

    source.shutdown()

    assert source.is_ready is False


def test_conversation_source_requires_ready_state() -> None:
    source = ConversationHistoryContextSource(
        lambda session_id: None
    )

    with pytest.raises(IntelligenceComponentStateError):
        source.collect_context(create_request())


def test_conversation_source_returns_empty_without_session_id() -> None:
    source = ConversationHistoryContextSource(
        lambda session_id: None
    )
    source.initialize()

    assert source.collect_context(
        create_request(session_id=None)
    ) == ()


def test_conversation_source_returns_empty_for_missing_session() -> None:
    source = ConversationHistoryContextSource(
        lambda session_id: None
    )
    source.initialize()

    assert source.collect_context(create_request()) == ()


def test_conversation_source_maps_all_roles() -> None:
    roles = (
        ConversationRole.SYSTEM,
        ConversationRole.USER,
        ConversationRole.ASSISTANT,
        ConversationRole.MEMORY,
        ConversationRole.TOOL_RESULT,
    )
    session = create_session(roles=roles)
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    items = source.collect_context(create_request())

    assert len(items) == 5
    assert items[0].trust_level is ContextTrustLevel.TRUSTED_SYSTEM
    assert items[1].trust_level is ContextTrustLevel.USER_PROVIDED
    assert (
        items[2].trust_level
        is ContextTrustLevel.TRUSTED_INTERNAL
    )
    assert (
        items[3].trust_level
        is ContextTrustLevel.RETRIEVED_MEMORY
    )
    assert items[3].context_type is IntelligenceContextType.MEMORY
    assert (
        items[4].context_type
        is IntelligenceContextType.TOOL_RESULT
    )


def test_system_turn_becomes_protected_context() -> None:
    session = create_session(
        roles=(ConversationRole.SYSTEM,)
    )
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert item.metadata["required_context"] is True
    assert item.trust_level is ContextTrustLevel.TRUSTED_SYSTEM


def test_conversation_source_preserves_provenance() -> None:
    session = create_session(
        roles=(ConversationRole.TOOL_RESULT,)
    )
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert item.metadata["session_id"] == "session-001"
    assert item.metadata["conversation_role"] == "tool_result"
    assert item.metadata["source_context_ids"] == ["source-0"]
    assert item.metadata["tool_result_ids"] == ["tool-0"]


def test_conversation_source_limits_history_window() -> None:
    session = create_session(
        roles=(
            ConversationRole.SYSTEM,
            ConversationRole.USER,
            ConversationRole.ASSISTANT,
            ConversationRole.USER,
        )
    )
    source = ConversationHistoryContextSource(
        lambda session_id: session,
        max_turns=2,
    )
    source.initialize()

    items = source.collect_context(create_request())

    assert len(items) == 2
    assert items[0].content == "assistant content"
    assert items[1].content == "user content"


def test_conversation_source_scores_recent_turn_higher() -> None:
    session = create_session(
        roles=(
            ConversationRole.USER,
            ConversationRole.ASSISTANT,
            ConversationRole.USER,
        )
    )
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    items = source.collect_context(create_request())

    assert items[0].relevance < items[1].relevance
    assert items[1].relevance < items[2].relevance
    assert items[2].relevance == pytest.approx(1.0)


def test_conversation_source_rejects_identity_mismatch() -> None:
    session = create_session(
        identity=create_identity("another-user")
    )
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_conversation_source_rejects_session_id_mismatch() -> None:
    session = create_session(session_id="different-session")
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_conversation_source_wraps_resolver_failure() -> None:
    def failing_resolver(
        session_id: str,
    ) -> ConversationSession | None:
        raise RuntimeError("session store unavailable")

    source = ConversationHistoryContextSource(
        failing_resolver
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_conversation_source_rejects_invalid_resolver_result() -> None:
    source = ConversationHistoryContextSource(
        lambda session_id: "invalid session"
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


@pytest.mark.parametrize("max_turns", [0, -1])
def test_conversation_source_requires_positive_history_window(
    max_turns: int,
) -> None:
    with pytest.raises(ValueError):
        ConversationHistoryContextSource(
            lambda session_id: None,
            max_turns=max_turns,
        )


def test_conversation_source_integrates_with_context_manager() -> None:
    session = create_session()
    source = ConversationHistoryContextSource(
        lambda session_id: session
    )
    source.initialize()

    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.initialize()

    bundle = manager.assemble_context(create_request())

    assert len(bundle.items) == 3
    assert bundle.metadata["registered_source_count"] == 1
    assert bundle.metadata["source_errors"] == {}
    assert any(
        item.metadata["conversation_role"] == "system"
        for item in bundle.items
    )