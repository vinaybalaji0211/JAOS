"""Tests for deterministic conversation reference resolution."""

from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ConversationRole,
    ConversationSession,
    ConversationSessionState,
    ConversationTurn,
    IntelligenceConversationError,
    IntelligenceIdentity,
    IntelligenceScope,
)
from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_reference_resolver import (
    ConversationReferenceResolution,
    ConversationReferenceResolutionState,
    ConversationReferenceResolver,
)

BASE_TIME = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)


def create_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


def create_turn(
    *,
    turn_id: str,
    content: str = "Conversation content",
    session_id: str = "session-1",
    created_at: datetime = BASE_TIME,
) -> ConversationTurn:
    return ConversationTurn(
        session_id=session_id,
        role=ConversationRole.USER,
        content=content,
        source="user",
        turn_id=turn_id,
        created_at=created_at,
    )


def create_session(
    *turns: ConversationTurn,
    session_id: str = "session-1",
) -> ConversationSession:
    updated_at = max(
        (turn.created_at for turn in turns),
        default=BASE_TIME,
    )

    return ConversationSession(
        identity=create_identity(),
        session_id=session_id,
        state=ConversationSessionState.ACTIVE,
        turns=tuple(turns),
        max_history_turns=100,
        context_policy="default",
        created_at=BASE_TIME - timedelta(minutes=1),
        updated_at=updated_at,
    )


def create_policy(
    *,
    allow_reference_resolution: bool = True,
    reference_window_turns: int = 20,
) -> ConversationPolicy:
    return ConversationPolicy(
        allow_reference_resolution=allow_reference_resolution,
        max_history_turns=100,
        reference_window_turns=reference_window_turns,
    )


def test_resolution_normalizes_and_serializes_values() -> None:
    candidate = create_turn(turn_id="turn-1")

    resolution = ConversationReferenceResolution(
        state=ConversationReferenceResolutionState.RESOLVED,
        query_turn_id=" query-turn ",
        strategy=" Explicit_Turn ",
        matched_markers=(" This ", "this"),
        candidate_turns=[candidate],
        unresolved_reference_ids=(" Missing ", "missing"),
    )

    assert resolution.query_turn_id == "query-turn"
    assert resolution.strategy == "explicit_turn"
    assert resolution.matched_markers == ("this",)
    assert resolution.candidate_turns == (candidate,)
    assert resolution.unresolved_reference_ids == ("missing",)
    assert resolution.reference_detected is True
    assert resolution.resolved is True
    assert resolution.to_dict() == {
        "state": "resolved",
        "query_turn_id": "query-turn",
        "strategy": "explicit_turn",
        "reference_detected": True,
        "resolved": True,
        "matched_markers": ["this"],
        "candidate_turn_ids": ["turn-1"],
        "unresolved_reference_ids": ["missing"],
    }


def test_not_required_resolution_properties() -> None:
    resolution = ConversationReferenceResolution(
        state=ConversationReferenceResolutionState.NOT_REQUIRED,
        query_turn_id="query-turn",
        strategy="none",
    )

    assert resolution.reference_detected is False
    assert resolution.resolved is False


def test_resolution_rejects_invalid_state() -> None:
    with pytest.raises(
        TypeError,
        match="ConversationReferenceResolutionState",
    ):
        ConversationReferenceResolution(
            state="resolved",
            query_turn_id="query-turn",
            strategy="explicit_turn",
        )


def test_resolution_rejects_empty_query_turn_id() -> None:
    with pytest.raises(
        ValueError,
        match="query_turn_id",
    ):
        ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id=" ",
            strategy="explicit_turn",
        )


def test_resolution_rejects_empty_strategy() -> None:
    with pytest.raises(
        ValueError,
        match="strategy",
    ):
        ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id="query-turn",
            strategy=" ",
        )


def test_resolution_rejects_invalid_marker() -> None:
    with pytest.raises(
        TypeError,
        match="matched_markers",
    ):
        ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id="query-turn",
            strategy="implicit_recent",
            matched_markers=("this", 10),
        )


def test_resolution_rejects_invalid_candidate_turn() -> None:
    with pytest.raises(
        TypeError,
        match="ConversationTurn",
    ):
        ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id="query-turn",
            strategy="implicit_recent",
            candidate_turns=("invalid",),
        )


def test_resolver_rejects_invalid_session() -> None:
    resolver = ConversationReferenceResolver()
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
    )

    with pytest.raises(
        TypeError,
        match="ConversationSession",
    ):
        resolver.resolve(
            "invalid",
            query,
            create_policy(),
        )


def test_resolver_rejects_invalid_query_turn() -> None:
    resolver = ConversationReferenceResolver()

    with pytest.raises(
        TypeError,
        match="ConversationTurn",
    ):
        resolver.resolve(
            create_session(),
            "invalid",
            create_policy(),
        )


def test_resolver_rejects_invalid_policy() -> None:
    resolver = ConversationReferenceResolver()
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
    )

    with pytest.raises(
        TypeError,
        match="ConversationPolicy",
    ):
        resolver.resolve(
            create_session(),
            query,
            "invalid",
        )


def test_resolver_rejects_mismatched_session() -> None:
    resolver = ConversationReferenceResolver()
    query = create_turn(
        session_id="another-session",
        turn_id="query-turn",
        content="Continue that",
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="does not match",
    ):
        resolver.resolve(
            create_session(),
            query,
            create_policy(),
        )


def test_query_without_reference_is_not_required() -> None:
    previous = create_turn(
        turn_id="turn-1",
        created_at=BASE_TIME,
    )
    query = create_turn(
        turn_id="query-turn",
        content="Explain the JAOS architecture",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.NOT_REQUIRED
    )
    assert resolution.strategy == "none"
    assert resolution.candidate_turns == ()
    assert resolution.reference_detected is False


def test_marker_is_not_detected_inside_another_word() -> None:
    query = create_turn(
        turn_id="query-turn",
        content="The iteration completed successfully",
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.NOT_REQUIRED
    )


def test_implicit_marker_detection_is_case_insensitive() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="CONTINUE THAT",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.RESOLVED
    )
    assert resolution.matched_markers == ("that", "continue")


def test_disabled_policy_reports_explicit_reference() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(allow_reference_resolution=False),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.DISABLED
    )
    assert resolution.strategy == "explicit_turn"
    assert resolution.candidate_turns == ()
    assert resolution.unresolved_reference_ids == ("turn-1",)


def test_disabled_policy_reports_implicit_reference() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(allow_reference_resolution=False),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.DISABLED
    )
    assert resolution.strategy == "implicit_recent"
    assert resolution.matched_markers == ("that", "continue")
    assert resolution.candidate_turns == ()


def test_explicit_reference_resolves_turn() -> None:
    first = create_turn(turn_id="turn-1")
    second = create_turn(
        turn_id="turn-2",
        created_at=BASE_TIME + timedelta(seconds=1),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=2),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(first, second),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.RESOLVED
    )
    assert resolution.strategy == "explicit_turn"
    assert resolution.candidate_turns == (first,)
    assert resolution.unresolved_reference_ids == ()


def test_multiple_explicit_references_preserve_query_order() -> None:
    first = create_turn(turn_id="turn-1")
    second = create_turn(
        turn_id="turn-2",
        created_at=BASE_TIME + timedelta(seconds=1),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Compare turn:turn-2 with turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=2),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(first, second),
        query,
        create_policy(),
    )

    assert resolution.candidate_turns == (second, first)


def test_duplicate_explicit_references_are_deduplicated() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="Compare turn:turn-1 with turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert resolution.candidate_turns == (previous,)


def test_missing_explicit_reference_is_unresolved() -> None:
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:missing-turn",
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.UNRESOLVED
    )
    assert resolution.candidate_turns == ()
    assert resolution.unresolved_reference_ids == (
        "missing-turn",
    )


def test_partially_resolved_explicit_references_are_auditable() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="Compare turn:turn-1 and turn:missing-turn",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.UNRESOLVED
    )
    assert resolution.candidate_turns == (previous,)
    assert resolution.unresolved_reference_ids == (
        "missing-turn",
    )


def test_explicit_reference_outside_window_is_unresolved() -> None:
    first = create_turn(turn_id="turn-1")
    second = create_turn(
        turn_id="turn-2",
        created_at=BASE_TIME + timedelta(seconds=1),
    )
    third = create_turn(
        turn_id="turn-3",
        created_at=BASE_TIME + timedelta(seconds=2),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=3),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(first, second, third),
        query,
        create_policy(reference_window_turns=2),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.UNRESOLVED
    )
    assert resolution.unresolved_reference_ids == ("turn-1",)


def test_explicit_reference_supports_safe_identifier_characters() -> None:
    previous = create_turn(turn_id="turn.alpha_2-final")
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:turn.alpha_2-final",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.RESOLVED
    )
    assert resolution.candidate_turns == (previous,)


def test_malformed_explicit_reference_is_not_detected() -> None:
    query = create_turn(
        turn_id="query-turn",
        content="Use turn:",
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.NOT_REQUIRED
    )


def test_implicit_reference_returns_eligible_prior_turns() -> None:
    first = create_turn(turn_id="turn-1")
    second = create_turn(
        turn_id="turn-2",
        created_at=BASE_TIME + timedelta(seconds=1),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
        created_at=BASE_TIME + timedelta(seconds=2),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(first, second),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.RESOLVED
    )
    assert resolution.strategy == "implicit_recent"
    assert resolution.candidate_turns == (first, second)


def test_implicit_reference_respects_reference_window() -> None:
    turns = tuple(
        create_turn(
            turn_id=f"turn-{index}",
            created_at=BASE_TIME + timedelta(seconds=index),
        )
        for index in range(1, 5)
    )
    query = create_turn(
        turn_id="query-turn",
        content="Continue this",
        created_at=BASE_TIME + timedelta(seconds=5),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(*turns),
        query,
        create_policy(reference_window_turns=2),
    )

    assert tuple(
        turn.turn_id for turn in resolution.candidate_turns
    ) == ("turn-3", "turn-4")


def test_implicit_reference_without_history_is_unresolved() -> None:
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(),
        query,
        create_policy(),
    )

    assert (
        resolution.state
        is ConversationReferenceResolutionState.UNRESOLVED
    )
    assert resolution.strategy == "implicit_recent"
    assert resolution.candidate_turns == ()


def test_query_turn_is_excluded_from_candidates() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous, query),
        query,
        create_policy(),
    )

    assert resolution.candidate_turns == (previous,)


def test_future_turn_is_excluded_from_candidates() -> None:
    previous = create_turn(turn_id="turn-1")
    future = create_turn(
        turn_id="turn-future",
        created_at=BASE_TIME + timedelta(seconds=10),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
        created_at=BASE_TIME + timedelta(seconds=5),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous, future),
        query,
        create_policy(),
    )

    assert resolution.candidate_turns == (previous,)


def test_turn_at_query_timestamp_is_eligible() -> None:
    previous = create_turn(
        turn_id="turn-1",
        created_at=BASE_TIME,
    )
    query = create_turn(
        turn_id="query-turn",
        content="Continue that",
        created_at=BASE_TIME,
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert resolution.candidate_turns == (previous,)


def test_explicit_reference_takes_priority_over_implicit_marker() -> None:
    first = create_turn(turn_id="turn-1")
    second = create_turn(
        turn_id="turn-2",
        created_at=BASE_TIME + timedelta(seconds=1),
    )
    query = create_turn(
        turn_id="query-turn",
        content="Continue that using turn:turn-1",
        created_at=BASE_TIME + timedelta(seconds=2),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(first, second),
        query,
        create_policy(),
    )

    assert resolution.strategy == "explicit_turn"
    assert resolution.candidate_turns == (first,)
    assert resolution.matched_markers == ("that", "continue")


def test_implicit_markers_follow_deterministic_registry_order() -> None:
    previous = create_turn(turn_id="turn-1")
    query = create_turn(
        turn_id="query-turn",
        content=(
            "Continue what you said earlier and do the same again"
        ),
        created_at=BASE_TIME + timedelta(seconds=1),
    )

    resolution = ConversationReferenceResolver().resolve(
        create_session(previous),
        query,
        create_policy(),
    )

    assert resolution.matched_markers == (
        "same",
        "earlier",
        "continue",
        "again",
        "what you said",
    )


def test_serialized_lists_do_not_mutate_resolution() -> None:
    previous = create_turn(turn_id="turn-1")

    resolution = ConversationReferenceResolution(
        state=ConversationReferenceResolutionState.RESOLVED,
        query_turn_id="query-turn",
        strategy="explicit_turn",
        matched_markers=("this",),
        candidate_turns=(previous,),
    )

    serialized = resolution.to_dict()
    serialized["matched_markers"].append("changed")
    serialized["candidate_turn_ids"].append("changed")

    assert resolution.matched_markers == ("this",)
    assert resolution.candidate_turns == (previous,)