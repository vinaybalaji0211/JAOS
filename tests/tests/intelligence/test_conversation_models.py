"""Tests for AI Intelligence Platform conversation models."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ConversationRole,
    ConversationSession,
    ConversationSessionState,
    ConversationTurn,
    IntelligenceIdentity,
    IntelligenceScope,
)


@pytest.fixture
def user_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


def test_conversation_turn_normalizes_valid_input() -> None:
    payload = {"intent": "continue"}
    metadata = {"source": "cli"}

    turn = ConversationTurn(
        session_id=" session-001 ",
        role=ConversationRole.USER,
        content=" Continue JAOS ",
        source=" CLI ",
        turn_id=" turn-001 ",
        structured_payload=payload,
        context_source_ids=(" memory-001 ", "memory-001"),
        tool_result_ids=(" tool-001 ",),
        metadata=metadata,
    )

    payload["intent"] = "changed"
    metadata["source"] = "changed"

    assert turn.session_id == "session-001"
    assert turn.turn_id == "turn-001"
    assert turn.content == "Continue JAOS"
    assert turn.source == "cli"
    assert turn.structured_payload == {"intent": "continue"}
    assert turn.context_source_ids == ("memory-001",)
    assert turn.tool_result_ids == ("tool-001",)
    assert turn.metadata == {"source": "cli"}
    assert turn.created_at.tzinfo is not None


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("turn_id", ""),
        ("session_id", "   "),
        ("content", ""),
        ("source", None),
    ],
)
def test_conversation_turn_rejects_invalid_required_string(
    field_name: str,
    value: object,
) -> None:
    arguments = {
        "turn_id": "turn-001",
        "session_id": "session-001",
        "role": ConversationRole.USER,
        "content": "Continue JAOS",
        "source": "conversation",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        ConversationTurn(**arguments)  # type: ignore[arg-type]


def test_conversation_turn_rejects_invalid_role() -> None:
    with pytest.raises(
        TypeError,
        match="role must be an instance of ConversationRole",
    ):
        ConversationTurn(
            session_id="session-001",
            role="user",  # type: ignore[arg-type]
            content="Continue JAOS",
        )


def test_conversation_turn_rejects_invalid_structured_payload() -> None:
    with pytest.raises(
        TypeError,
        match="structured_payload must be a dictionary",
    ):
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="Continue JAOS",
            structured_payload=[],  # type: ignore[arg-type]
        )


def test_conversation_turn_rejects_invalid_metadata() -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="Continue JAOS",
            metadata=[],  # type: ignore[arg-type]
        )


def test_conversation_turn_rejects_naive_created_at() -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="Continue JAOS",
            created_at=datetime(2026, 1, 1),
        )


def test_conversation_turn_rejects_string_identifier_collection() -> None:
    with pytest.raises(
        TypeError,
        match="context_source_ids must be a collection",
    ):
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="Continue JAOS",
            context_source_ids="memory-001",  # type: ignore[arg-type]
        )


def test_conversation_turn_rejects_empty_identifier() -> None:
    with pytest.raises(
        ValueError,
        match="tool_result_ids must contain only non-empty strings",
    ):
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.TOOL_RESULT,
            content="Tool completed",
            tool_result_ids=("tool-001", "   "),
        )


def test_conversation_turn_to_dict_is_json_serializable() -> None:
    turn = ConversationTurn(
        session_id="session-001",
        role=ConversationRole.ASSISTANT,
        content="JAOS continued",
        turn_id="turn-001",
        context_source_ids=("memory-001",),
    )

    decoded = json.loads(json.dumps(turn.to_dict()))

    assert decoded["turn_id"] == "turn-001"
    assert decoded["session_id"] == "session-001"
    assert decoded["role"] == "assistant"
    assert decoded["content"] == "JAOS continued"
    assert decoded["context_source_ids"] == ["memory-001"]


def test_conversation_turn_is_immutable() -> None:
    turn = ConversationTurn(
        session_id="session-001",
        role=ConversationRole.USER,
        content="Continue JAOS",
    )

    with pytest.raises(FrozenInstanceError):
        turn.content = "Changed"  # type: ignore[misc]


def test_conversation_session_accepts_minimum_valid_input(
    user_identity: IntelligenceIdentity,
) -> None:
    session = ConversationSession(
        identity=user_identity,
        session_id="session-001",
    )

    assert session.identity is user_identity
    assert session.session_id == "session-001"
    assert session.state is ConversationSessionState.ACTIVE
    assert session.turns == ()
    assert session.max_history_turns == 100
    assert session.created_at.tzinfo is not None
    assert session.updated_at.tzinfo is not None


def test_conversation_session_accepts_matching_turns(
    user_identity: IntelligenceIdentity,
) -> None:
    turn = ConversationTurn(
        session_id="session-001",
        role=ConversationRole.USER,
        content="Continue JAOS",
    )

    metadata = {"channel": "cli"}

    session = ConversationSession(
        identity=user_identity,
        session_id=" session-001 ",
        turns=[turn],  # type: ignore[arg-type]
        context_policy=" DEFAULT ",
        metadata=metadata,
    )

    metadata["channel"] = "changed"

    assert session.session_id == "session-001"
    assert session.turns == (turn,)
    assert session.context_policy == "default"
    assert session.metadata == {"channel": "cli"}


def test_conversation_session_rejects_mismatched_turn(
    user_identity: IntelligenceIdentity,
) -> None:
    turn = ConversationTurn(
        session_id="another-session",
        role=ConversationRole.USER,
        content="Continue JAOS",
    )

    with pytest.raises(
        ValueError,
        match="every conversation turn must match session_id",
    ):
        ConversationSession(
            identity=user_identity,
            session_id="session-001",
            turns=(turn,),
        )


def test_conversation_session_rejects_invalid_turn_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="turns must contain only ConversationTurn instances",
    ):
        ConversationSession(
            identity=user_identity,
            turns=("invalid",),  # type: ignore[arg-type]
        )


def test_conversation_session_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an instance of IntelligenceIdentity",
    ):
        ConversationSession(
            identity="vinay",  # type: ignore[arg-type]
        )


def test_conversation_session_rejects_invalid_state(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="state must be an instance of ConversationSessionState",
    ):
        ConversationSession(
            identity=user_identity,
            state="active",  # type: ignore[arg-type]
        )


def test_conversation_session_rejects_boolean_history_limit(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_history_turns must be an integer",
    ):
        ConversationSession(
            identity=user_identity,
            max_history_turns=True,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("max_history_turns", [0, -1])
def test_conversation_session_rejects_non_positive_history_limit(
    max_history_turns: int,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_history_turns must be greater than zero",
    ):
        ConversationSession(
            identity=user_identity,
            max_history_turns=max_history_turns,
        )


def test_conversation_session_rejects_excess_turns(
    user_identity: IntelligenceIdentity,
) -> None:
    turns = (
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="First",
        ),
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.ASSISTANT,
            content="Second",
        ),
    )

    with pytest.raises(
        ValueError,
        match="conversation turns exceed max_history_turns",
    ):
        ConversationSession(
            identity=user_identity,
            session_id="session-001",
            turns=turns,
            max_history_turns=1,
        )


def test_conversation_session_rejects_unordered_turns(
    user_identity: IntelligenceIdentity,
) -> None:
    first_time = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
    second_time = first_time - timedelta(minutes=1)

    turns = (
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.USER,
            content="First",
            created_at=first_time,
        ),
        ConversationTurn(
            session_id="session-001",
            role=ConversationRole.ASSISTANT,
            content="Second",
            created_at=second_time,
        ),
    )

    with pytest.raises(
        ValueError,
        match="conversation turns must be ordered by created_at",
    ):
        ConversationSession(
            identity=user_identity,
            session_id="session-001",
            turns=turns,
        )


def test_conversation_session_rejects_invalid_context_policy(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="context_policy must be a string or None",
    ):
        ConversationSession(
            identity=user_identity,
            context_policy=123,  # type: ignore[arg-type]
        )


def test_conversation_session_rejects_invalid_metadata(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        ConversationSession(
            identity=user_identity,
            metadata=[],  # type: ignore[arg-type]
        )


def test_conversation_session_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        ConversationSession(
            identity=user_identity,
            created_at=datetime(2026, 1, 1),
        )


def test_conversation_session_rejects_naive_updated_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="updated_at must be timezone-aware",
    ):
        ConversationSession(
            identity=user_identity,
            updated_at=datetime(2026, 1, 1),
        )


def test_conversation_session_rejects_invalid_timestamp_order(
    user_identity: IntelligenceIdentity,
) -> None:
    created_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
    updated_at = created_at - timedelta(days=1)

    with pytest.raises(
        ValueError,
        match="updated_at must not be earlier than created_at",
    ):
        ConversationSession(
            identity=user_identity,
            created_at=created_at,
            updated_at=updated_at,
        )


def test_conversation_session_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
) -> None:
    turn = ConversationTurn(
        session_id="session-001",
        role=ConversationRole.USER,
        content="Continue JAOS",
        turn_id="turn-001",
    )

    session = ConversationSession(
        identity=user_identity,
        session_id="session-001",
        turns=(turn,),
        context_policy="default",
    )

    decoded = json.loads(json.dumps(session.to_dict()))

    assert decoded["session_id"] == "session-001"
    assert decoded["identity"] == {
        "scope": "user",
        "identity_id": "vinay",
    }
    assert decoded["state"] == "active"
    assert decoded["turns"][0]["turn_id"] == "turn-001"


def test_conversation_session_is_immutable(
    user_identity: IntelligenceIdentity,
) -> None:
    session = ConversationSession(identity=user_identity)

    with pytest.raises(FrozenInstanceError):
        session.state = (  # type: ignore[misc]
            ConversationSessionState.CLOSED
        )