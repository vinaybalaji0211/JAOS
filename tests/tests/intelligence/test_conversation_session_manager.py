"""Tests for conversation session lifecycle management."""

from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ConversationRole,
    ConversationSessionState,
    ConversationTurn,
    IntelligenceConversationError,
    IntelligenceIdentity,
    IntelligencePermissionError,
    IntelligenceScope,
)
from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_policy_registry import (
    ConversationPolicyRegistry,
)
from jaos.intelligence.conversation.conversation_session_manager import (
    ConversationSessionManager,
)
from jaos.intelligence.conversation.in_memory_conversation_session_store import (
    InMemoryConversationSessionStore,
)

BASE_TIME = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)


def fixed_clock() -> datetime:
    return BASE_TIME


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_turn(
    *,
    session_id: str = "session-1",
    turn_id: str = "turn-1",
    content: str = "Hello JAOS",
    created_at: datetime = BASE_TIME + timedelta(seconds=1),
) -> ConversationTurn:
    return ConversationTurn(
        session_id=session_id,
        role=ConversationRole.USER,
        content=content,
        source="user",
        turn_id=turn_id,
        created_at=created_at,
    )


def create_manager(
    *,
    policy_name: str = "default",
    max_history_turns: int = 100,
    allow_interruption: bool = True,
    allow_continuation: bool = True,
) -> tuple[
    ConversationSessionManager,
    InMemoryConversationSessionStore,
    ConversationPolicyRegistry,
]:
    registry = ConversationPolicyRegistry()
    registry.register_policy(
        ConversationPolicy(
            policy_name=policy_name,
            context_policy="default",
            max_history_turns=max_history_turns,
            reference_window_turns=min(
                20,
                max_history_turns,
            ),
            allow_interruption=allow_interruption,
            allow_continuation=allow_continuation,
        ),
        make_default=True,
    )

    store = InMemoryConversationSessionStore()
    manager = ConversationSessionManager(
        store,
        registry,
        clock=fixed_clock,
    )

    return manager, store, registry


def test_manager_rejects_invalid_session_store() -> None:
    with pytest.raises(
        TypeError,
        match="session_store",
    ):
        ConversationSessionManager(
            "invalid",
            ConversationPolicyRegistry(),
        )


def test_manager_rejects_invalid_policy_registry() -> None:
    with pytest.raises(
        TypeError,
        match="policy_registry",
    ):
        ConversationSessionManager(
            InMemoryConversationSessionStore(),
            "invalid",
        )


def test_start_session_uses_default_policy() -> None:
    manager, store, _ = create_manager()
    metadata = {"owner": "vinay"}

    session = manager.start_session(
        create_identity(),
        session_id="session-1",
        metadata=metadata,
    )

    metadata["owner"] = "changed"

    assert session.session_id == "session-1"
    assert session.state is ConversationSessionState.ACTIVE
    assert session.max_history_turns == 100
    assert session.context_policy == "default"
    assert session.metadata == {
        "owner": "vinay",
        "conversation_policy": "default",
    }
    assert session.created_at == BASE_TIME
    assert session.updated_at == BASE_TIME
    assert store.get_session("session-1") == session


def test_start_session_uses_explicit_policy() -> None:
    registry = ConversationPolicyRegistry()
    registry.register_policy(
        ConversationPolicy(policy_name="default"),
        make_default=True,
    )
    registry.register_policy(
        ConversationPolicy(
            policy_name="focused",
            context_policy="strict",
            max_history_turns=5,
            reference_window_turns=3,
        )
    )

    store = InMemoryConversationSessionStore()
    manager = ConversationSessionManager(
        store,
        registry,
        clock=fixed_clock,
    )

    session = manager.start_session(
        create_identity(),
        policy_name="focused",
        session_id="focused-session",
    )

    assert session.max_history_turns == 5
    assert session.context_policy == "strict"
    assert session.metadata["conversation_policy"] == "focused"


def test_start_session_generates_identifier() -> None:
    manager, store, _ = create_manager()

    session = manager.start_session(create_identity())

    assert isinstance(session.session_id, str)
    assert session.session_id
    assert store.contains(session.session_id) is True


def test_start_session_rejects_duplicate_identifier() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="already exists",
    ):
        manager.start_session(
            create_identity(),
            session_id="session-1",
        )


def test_start_session_rejects_invalid_identity() -> None:
    manager, _, _ = create_manager()

    with pytest.raises(
        TypeError,
        match="identity",
    ):
        manager.start_session(
            "vinay",
            session_id="session-1",
        )


def test_start_session_rejects_invalid_metadata() -> None:
    manager, _, _ = create_manager()

    with pytest.raises(
        TypeError,
        match="metadata",
    ):
        manager.start_session(
            create_identity(),
            session_id="session-1",
            metadata="invalid",
        )


def test_get_required_session_rejects_missing_session() -> None:
    manager, _, _ = create_manager()

    with pytest.raises(
        IntelligenceConversationError,
        match="session not found",
    ):
        manager.get_required_session("missing")


def test_session_access_enforces_identity_isolation() -> None:
    manager, _, _ = create_manager()
    owner = create_identity("vinay")
    another_user = create_identity("another-user")

    manager.start_session(
        owner,
        session_id="session-1",
    )

    assert (
        manager.get_session(
            "session-1",
            identity=owner,
        )
        is not None
    )

    with pytest.raises(
        IntelligencePermissionError,
        match="access denied",
    ):
        manager.get_session(
            "session-1",
            identity=another_user,
        )


def test_append_turn_updates_active_session() -> None:
    manager, store, _ = create_manager()
    identity = create_identity()

    manager.start_session(
        identity,
        session_id="session-1",
    )

    turn = create_turn()
    updated = manager.append_turn(
        "session-1",
        turn,
        identity=identity,
    )

    assert updated.turns == (turn,)
    assert updated.updated_at == turn.created_at
    assert store.get_session("session-1") == updated


def test_append_turn_rejects_invalid_turn_type() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    with pytest.raises(
        TypeError,
        match="ConversationTurn",
    ):
        manager.append_turn(
            "session-1",
            "invalid",
        )


def test_append_turn_rejects_mismatched_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="does not match",
    ):
        manager.append_turn(
            "session-1",
            create_turn(session_id="another-session"),
        )


def test_append_turn_rejects_turn_before_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    turn = create_turn(
        created_at=BASE_TIME - timedelta(seconds=1),
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="predates",
    ):
        manager.append_turn("session-1", turn)


def test_append_turn_rejects_duplicate_turn() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    turn = create_turn()
    manager.append_turn("session-1", turn)

    with pytest.raises(
        IntelligenceConversationError,
        match="already exists",
    ):
        manager.append_turn("session-1", turn)


def test_append_turn_rejects_out_of_order_turn() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    manager.append_turn(
        "session-1",
        create_turn(
            turn_id="turn-2",
            created_at=BASE_TIME + timedelta(seconds=2),
        ),
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="out of order",
    ):
        manager.append_turn(
            "session-1",
            create_turn(
                turn_id="turn-1",
                created_at=BASE_TIME + timedelta(seconds=1),
            ),
        )


def test_append_turn_truncates_bounded_history() -> None:
    manager, _, _ = create_manager(max_history_turns=2)

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    for index in range(1, 4):
        manager.append_turn(
            "session-1",
            create_turn(
                turn_id=f"turn-{index}",
                created_at=(
                    BASE_TIME + timedelta(seconds=index)
                ),
            ),
        )

    session = manager.get_required_session("session-1")

    assert tuple(
        turn.turn_id for turn in session.turns
    ) == ("turn-2", "turn-3")
    assert session.metadata["history_truncated_count"] == 1


def test_append_turn_rejects_non_active_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.close_session("session-1")

    with pytest.raises(
        IntelligenceConversationError,
        match="invalid state",
    ):
        manager.append_turn(
            "session-1",
            create_turn(),
        )


def test_interrupt_session_records_reason() -> None:
    manager, _, _ = create_manager()
    identity = create_identity()

    manager.start_session(
        identity,
        session_id="session-1",
    )

    interrupted = manager.interrupt_session(
        "session-1",
        identity=identity,
        reason="  user paused interaction  ",
    )

    assert (
        interrupted.state
        is ConversationSessionState.INTERRUPTED
    )
    assert (
        interrupted.metadata["interruption_reason"]
        == "user paused interaction"
    )
    assert (
        interrupted.metadata["interrupted_at"]
        == interrupted.updated_at.isoformat()
    )


def test_interrupt_session_obeys_policy() -> None:
    manager, _, _ = create_manager(
        allow_interruption=False,
    )

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="does not allow interruption",
    ):
        manager.interrupt_session("session-1")


def test_interrupt_session_requires_active_state() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.interrupt_session("session-1")

    with pytest.raises(
        IntelligenceConversationError,
        match="invalid state",
    ):
        manager.interrupt_session("session-1")


def test_continue_session_restores_active_state() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.interrupt_session("session-1")

    first_continuation = manager.continue_session("session-1")

    assert (
        first_continuation.state
        is ConversationSessionState.ACTIVE
    )
    assert first_continuation.metadata["continuation_count"] == 1

    manager.interrupt_session("session-1")
    second_continuation = manager.continue_session("session-1")

    assert second_continuation.metadata["continuation_count"] == 2
    assert (
        second_continuation.metadata["continued_at"]
        == second_continuation.updated_at.isoformat()
    )


def test_continue_session_requires_interrupted_state() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="invalid state",
    ):
        manager.continue_session("session-1")


def test_continue_session_obeys_policy() -> None:
    manager, _, _ = create_manager(
        allow_continuation=False,
    )

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.interrupt_session("session-1")

    with pytest.raises(
        IntelligenceConversationError,
        match="does not allow continuation",
    ):
        manager.continue_session("session-1")


def test_close_active_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    closed = manager.close_session("session-1")

    assert closed.state is ConversationSessionState.CLOSED
    assert (
        closed.metadata["closed_at"]
        == closed.updated_at.isoformat()
    )


def test_close_interrupted_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.interrupt_session("session-1")

    closed = manager.close_session("session-1")

    assert closed.state is ConversationSessionState.CLOSED


def test_close_session_is_idempotent() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    first = manager.close_session("session-1")
    second = manager.close_session("session-1")

    assert second == first
    assert second.updated_at == first.updated_at


def test_fail_active_session_records_reason() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )

    failed = manager.fail_session(
        "session-1",
        "  provider response failed  ",
    )

    assert failed.state is ConversationSessionState.FAILED
    assert (
        failed.metadata["failure_reason"]
        == "provider response failed"
    )
    assert (
        failed.metadata["failed_at"]
        == failed.updated_at.isoformat()
    )


def test_fail_interrupted_session() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.interrupt_session("session-1")

    failed = manager.fail_session(
        "session-1",
        "runtime shutdown",
    )

    assert failed.state is ConversationSessionState.FAILED


def test_failed_session_cannot_be_closed() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.fail_session(
        "session-1",
        "provider failure",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="cannot be closed",
    ):
        manager.close_session("session-1")


def test_closed_session_cannot_be_failed() -> None:
    manager, _, _ = create_manager()

    manager.start_session(
        create_identity(),
        session_id="session-1",
    )
    manager.close_session("session-1")

    with pytest.raises(
        IntelligenceConversationError,
        match="cannot be failed",
    ):
        manager.fail_session(
            "session-1",
            "late failure",
        )


def test_list_sessions_filters_identity_and_state() -> None:
    manager, _, _ = create_manager()
    vinay = create_identity("vinay")
    another_user = create_identity("another-user")

    manager.start_session(
        vinay,
        session_id="vinay-active",
    )
    manager.start_session(
        vinay,
        session_id="vinay-closed",
    )
    manager.start_session(
        another_user,
        session_id="other-active",
    )

    manager.close_session("vinay-closed")

    sessions = manager.list_sessions(
        identity=vinay,
        state=ConversationSessionState.CLOSED,
    )

    assert tuple(
        session.session_id for session in sessions
    ) == ("vinay-closed",)


def test_manager_requires_timezone_aware_clock() -> None:
    manager, _, _ = create_manager()
    manager._clock = lambda: datetime(2026, 7, 20, 12, 0)

    with pytest.raises(
        ValueError,
        match="timezone-aware",
    ):
        manager.start_session(
            create_identity(),
            session_id="session-1",
        )