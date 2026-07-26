"""Tests for conversation session storage contracts."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ConversationSession,
    ConversationSessionState,
    IntelligenceConversationError,
    IntelligenceIdentity,
    IntelligenceScope,
)
from jaos.intelligence.conversation.conversation_session_store import (
    ConversationSessionStore,
)
from jaos.intelligence.conversation.in_memory_conversation_session_store import (
    InMemoryConversationSessionStore,
)


BASE_TIME = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_session(
    *,
    session_id: str = "session-1",
    identity: IntelligenceIdentity | None = None,
    state: ConversationSessionState = (
        ConversationSessionState.ACTIVE
    ),
    created_at: datetime = BASE_TIME,
    updated_at: datetime = BASE_TIME,
    metadata: dict[str, object] | None = None,
) -> ConversationSession:
    return ConversationSession(
        identity=identity or create_identity(),
        session_id=session_id,
        state=state,
        metadata=dict(metadata or {}),
        created_at=created_at,
        updated_at=updated_at,
    )


def test_session_store_contract_is_abstract() -> None:
    with pytest.raises(TypeError):
        ConversationSessionStore()


def test_new_store_is_empty() -> None:
    store = InMemoryConversationSessionStore()

    assert len(store) == 0
    assert store.get_session("missing") is None
    assert store.list_sessions() == ()
    assert store.contains("missing") is False


def test_store_saves_and_returns_session_snapshot() -> None:
    store = InMemoryConversationSessionStore()
    session = create_session()

    saved = store.save_session(session)
    loaded = store.get_session(session.session_id)

    assert saved == session
    assert loaded == session
    assert saved is not session
    assert loaded is not session
    assert len(store) == 1


def test_store_defensively_isolates_mutable_metadata() -> None:
    store = InMemoryConversationSessionStore()
    session = create_session(metadata={"owner": "jaos"})

    saved = store.save_session(session)

    session.metadata["owner"] = "changed-original"
    saved.metadata["owner"] = "changed-return-value"

    loaded = store.get_session(session.session_id)

    assert loaded is not None
    assert loaded.metadata == {"owner": "jaos"}


def test_store_can_replace_snapshot_without_concurrency_check() -> None:
    store = InMemoryConversationSessionStore()
    original = create_session(metadata={"revision": 1})
    updated = replace(
        original,
        updated_at=BASE_TIME + timedelta(seconds=1),
        metadata={"revision": 2},
    )

    store.save_session(original)
    store.save_session(updated)

    assert store.get_session(original.session_id) == updated
    assert len(store) == 1


def test_store_accepts_matching_optimistic_concurrency_time() -> None:
    store = InMemoryConversationSessionStore()
    original = create_session()
    updated = replace(
        original,
        updated_at=BASE_TIME + timedelta(seconds=1),
    )

    store.save_session(original)
    saved = store.save_session(
        updated,
        expected_updated_at=original.updated_at,
    )

    assert saved == updated
    assert store.get_session(original.session_id) == updated


def test_store_rejects_stale_snapshot_update() -> None:
    store = InMemoryConversationSessionStore()
    original = create_session()
    first_update = replace(
        original,
        updated_at=BASE_TIME + timedelta(seconds=1),
    )
    stale_update = replace(
        original,
        updated_at=BASE_TIME + timedelta(seconds=2),
    )

    store.save_session(original)
    store.save_session(
        first_update,
        expected_updated_at=original.updated_at,
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="concurrency check failed",
    ) as error:
        store.save_session(
            stale_update,
            expected_updated_at=original.updated_at,
        )

    assert error.value.details["reason"] == "stale_snapshot"
    assert error.value.details["session_id"] == "session-1"


def test_store_rejects_expected_time_for_missing_session() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        IntelligenceConversationError,
        match="concurrency check failed",
    ) as error:
        store.save_session(
            create_session(),
            expected_updated_at=BASE_TIME,
        )

    assert error.value.details["reason"] == "session_not_found"


def test_store_rejects_naive_expected_timestamp() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        ValueError,
        match="timezone-aware",
    ):
        store.save_session(
            create_session(),
            expected_updated_at=datetime(2026, 7, 20, 12, 0),
        )


def test_store_lists_sessions_deterministically() -> None:
    store = InMemoryConversationSessionStore()
    second = create_session(
        session_id="session-2",
        created_at=BASE_TIME + timedelta(seconds=2),
        updated_at=BASE_TIME + timedelta(seconds=2),
    )
    first = create_session(
        session_id="session-1",
        created_at=BASE_TIME + timedelta(seconds=1),
        updated_at=BASE_TIME + timedelta(seconds=1),
    )

    store.save_session(second)
    store.save_session(first)

    assert tuple(
        session.session_id
        for session in store.list_sessions()
    ) == ("session-1", "session-2")


def test_store_filters_sessions_by_identity() -> None:
    store = InMemoryConversationSessionStore()
    vinay = create_identity("vinay")
    another_user = create_identity("another-user")

    store.save_session(
        create_session(
            session_id="vinay-session",
            identity=vinay,
        )
    )
    store.save_session(
        create_session(
            session_id="other-session",
            identity=another_user,
        )
    )

    sessions = store.list_sessions(identity=vinay)

    assert tuple(
        session.session_id for session in sessions
    ) == ("vinay-session",)


def test_store_filters_sessions_by_state() -> None:
    store = InMemoryConversationSessionStore()

    store.save_session(
        create_session(
            session_id="active-session",
            state=ConversationSessionState.ACTIVE,
        )
    )
    store.save_session(
        create_session(
            session_id="interrupted-session",
            state=ConversationSessionState.INTERRUPTED,
        )
    )

    sessions = store.list_sessions(
        state=ConversationSessionState.INTERRUPTED
    )

    assert tuple(
        session.session_id for session in sessions
    ) == ("interrupted-session",)


def test_store_deletes_and_returns_session() -> None:
    store = InMemoryConversationSessionStore()
    session = create_session()

    store.save_session(session)

    removed = store.delete_session(session.session_id)

    assert removed == session
    assert store.delete_session(session.session_id) is None
    assert store.get_session(session.session_id) is None
    assert len(store) == 0


def test_store_normalizes_session_id_for_lookup() -> None:
    store = InMemoryConversationSessionStore()
    store.save_session(create_session())

    assert store.contains(" session-1 ") is True
    assert store.get_session(" session-1 ") is not None


@pytest.mark.parametrize("session_id", ("", "   "))
def test_store_rejects_empty_session_id(
    session_id: str,
) -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        store.get_session(session_id)


def test_store_rejects_non_string_session_id() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        TypeError,
        match="must be a string",
    ):
        store.contains(123)


def test_store_rejects_invalid_session_type() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        TypeError,
        match="must be a ConversationSession",
    ):
        store.save_session("invalid")


def test_store_rejects_invalid_identity_filter() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        TypeError,
        match="identity",
    ):
        store.list_sessions(identity="vinay")


def test_store_rejects_invalid_state_filter() -> None:
    store = InMemoryConversationSessionStore()

    with pytest.raises(
        TypeError,
        match="state",
    ):
        store.list_sessions(state="active")