"""Safe conversation reference resolution for JAOS Intelligence."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.exceptions import IntelligenceConversationError
from jaos.intelligence.models import (
    ConversationSession,
    ConversationTurn,
)


class ConversationReferenceResolutionState(str, Enum):
    """Possible outcomes of conversation reference resolution."""

    NOT_REQUIRED = "not_required"
    DISABLED = "disabled"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class ConversationReferenceResolution:
    """Immutable result of one reference-resolution attempt."""

    state: ConversationReferenceResolutionState
    query_turn_id: str
    strategy: str
    matched_markers: tuple[str, ...] = ()
    candidate_turns: tuple[ConversationTurn, ...] = ()
    unresolved_reference_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate and isolate the resolution result."""

        if not isinstance(
            self.state,
            ConversationReferenceResolutionState,
        ):
            raise TypeError(
                "state must be a "
                "ConversationReferenceResolutionState"
            )

        if not isinstance(self.query_turn_id, str):
            raise TypeError("query_turn_id must be a string")

        query_turn_id = self.query_turn_id.strip()

        if not query_turn_id:
            raise ValueError("query_turn_id must not be empty")

        if not isinstance(self.strategy, str):
            raise TypeError("strategy must be a string")

        strategy = self.strategy.strip().lower()

        if not strategy:
            raise ValueError("strategy must not be empty")

        matched_markers = self._normalize_text_tuple(
            self.matched_markers,
            "matched_markers",
        )
        unresolved_reference_ids = self._normalize_text_tuple(
            self.unresolved_reference_ids,
            "unresolved_reference_ids",
        )

        try:
            candidate_turns = tuple(self.candidate_turns)
        except TypeError as error:
            raise TypeError(
                "candidate_turns must be an iterable of "
                "ConversationTurn values"
            ) from error

        for turn in candidate_turns:
            if not isinstance(turn, ConversationTurn):
                raise TypeError(
                    "candidate_turns must contain only "
                    "ConversationTurn values"
                )

        object.__setattr__(self, "query_turn_id", query_turn_id)
        object.__setattr__(self, "strategy", strategy)
        object.__setattr__(
            self,
            "matched_markers",
            matched_markers,
        )
        object.__setattr__(
            self,
            "candidate_turns",
            candidate_turns,
        )
        object.__setattr__(
            self,
            "unresolved_reference_ids",
            unresolved_reference_ids,
        )

    @property
    def reference_detected(self) -> bool:
        """Return whether the query contains a reference marker."""

        return bool(
            self.matched_markers
            or self.unresolved_reference_ids
            or self.strategy in {"explicit_turn", "implicit_recent"}
        )

    @property
    def resolved(self) -> bool:
        """Return whether reference candidates were resolved."""

        return (
            self.state
            is ConversationReferenceResolutionState.RESOLVED
        )

    def to_dict(self) -> dict[str, Any]:
        """Return an audit-friendly serialized representation."""

        return {
            "state": self.state.value,
            "query_turn_id": self.query_turn_id,
            "strategy": self.strategy,
            "reference_detected": self.reference_detected,
            "resolved": self.resolved,
            "matched_markers": list(self.matched_markers),
            "candidate_turn_ids": [
                turn.turn_id for turn in self.candidate_turns
            ],
            "unresolved_reference_ids": list(
                self.unresolved_reference_ids
            ),
        }

    @staticmethod
    def _normalize_text_tuple(
        values: tuple[str, ...],
        field_name: str,
    ) -> tuple[str, ...]:
        try:
            resolved_values = tuple(values)
        except TypeError as error:
            raise TypeError(
                f"{field_name} must be an iterable of strings"
            ) from error

        normalized_values: list[str] = []

        for value in resolved_values:
            if not isinstance(value, str):
                raise TypeError(
                    f"{field_name} must contain only strings"
                )

            normalized = value.strip().lower()

            if not normalized:
                raise ValueError(
                    f"{field_name} must not contain empty values"
                )

            if normalized not in normalized_values:
                normalized_values.append(normalized)

        return tuple(normalized_values)


class ConversationReferenceResolver:
    """
    Resolves explicit and implicit references to eligible prior turns.

    The resolver is deterministic and provider-independent. It identifies
    candidate turns only; semantic interpretation remains the responsibility
    of the approved Context Manager and AI Platform workflow.
    """

    _EXPLICIT_TURN_PATTERN = re.compile(
        r"\bturn:([a-zA-Z0-9][a-zA-Z0-9_.-]{0,127})\b"
    )

    _IMPLICIT_MARKER_PATTERNS: tuple[
        tuple[str, re.Pattern[str]],
        ...,
    ] = (
        ("it", re.compile(r"\bit\b", re.IGNORECASE)),
        ("this", re.compile(r"\bthis\b", re.IGNORECASE)),
        ("that", re.compile(r"\bthat\b", re.IGNORECASE)),
        ("these", re.compile(r"\bthese\b", re.IGNORECASE)),
        ("those", re.compile(r"\bthose\b", re.IGNORECASE)),
        ("them", re.compile(r"\bthem\b", re.IGNORECASE)),
        ("same", re.compile(r"\bsame\b", re.IGNORECASE)),
        ("previous", re.compile(r"\bprevious\b", re.IGNORECASE)),
        ("earlier", re.compile(r"\bearlier\b", re.IGNORECASE)),
        ("above", re.compile(r"\babove\b", re.IGNORECASE)),
        ("continue", re.compile(r"\bcontinue\b", re.IGNORECASE)),
        ("again", re.compile(r"\bagain\b", re.IGNORECASE)),
        (
            "what you said",
            re.compile(r"\bwhat you said\b", re.IGNORECASE),
        ),
        (
            "that one",
            re.compile(r"\bthat one\b", re.IGNORECASE),
        ),
        (
            "do so",
            re.compile(r"\bdo so\b", re.IGNORECASE),
        ),
    )

    def resolve(
        self,
        session: ConversationSession,
        query_turn: ConversationTurn,
        policy: ConversationPolicy,
    ) -> ConversationReferenceResolution:
        """Resolve eligible prior-turn candidates for one query."""

        if not isinstance(session, ConversationSession):
            raise TypeError(
                "session must be a ConversationSession"
            )

        if not isinstance(query_turn, ConversationTurn):
            raise TypeError(
                "query_turn must be a ConversationTurn"
            )

        if not isinstance(policy, ConversationPolicy):
            raise TypeError(
                "policy must be a ConversationPolicy"
            )

        if query_turn.session_id != session.session_id:
            raise IntelligenceConversationError(
                "query turn session_id does not match session",
                component="conversation_reference_resolver",
                details={
                    "session_id": session.session_id,
                    "query_turn_id": query_turn.turn_id,
                    "query_session_id": query_turn.session_id,
                },
            )

        eligible_turns = self._eligible_turns(
            session,
            query_turn,
            policy.reference_window_turns,
        )
        explicit_reference_ids = (
            self._extract_explicit_reference_ids(
                query_turn.content
            )
        )
        matched_markers = self._find_implicit_markers(
            query_turn.content
        )

        if not explicit_reference_ids and not matched_markers:
            return ConversationReferenceResolution(
                state=(
                    ConversationReferenceResolutionState.NOT_REQUIRED
                ),
                query_turn_id=query_turn.turn_id,
                strategy="none",
            )

        if not policy.allow_reference_resolution:
            strategy = (
                "explicit_turn"
                if explicit_reference_ids
                else "implicit_recent"
            )

            return ConversationReferenceResolution(
                state=(
                    ConversationReferenceResolutionState.DISABLED
                ),
                query_turn_id=query_turn.turn_id,
                strategy=strategy,
                matched_markers=matched_markers,
                unresolved_reference_ids=explicit_reference_ids,
            )

        if explicit_reference_ids:
            return self._resolve_explicit_references(
                query_turn,
                eligible_turns,
                explicit_reference_ids,
                matched_markers,
            )

        if not eligible_turns:
            return ConversationReferenceResolution(
                state=(
                    ConversationReferenceResolutionState.UNRESOLVED
                ),
                query_turn_id=query_turn.turn_id,
                strategy="implicit_recent",
                matched_markers=matched_markers,
            )

        return ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id=query_turn.turn_id,
            strategy="implicit_recent",
            matched_markers=matched_markers,
            candidate_turns=eligible_turns,
        )

    @staticmethod
    def _eligible_turns(
        session: ConversationSession,
        query_turn: ConversationTurn,
        reference_window_turns: int,
    ) -> tuple[ConversationTurn, ...]:
        prior_turns = tuple(
            turn
            for turn in session.turns
            if turn.turn_id != query_turn.turn_id
            and turn.created_at <= query_turn.created_at
        )

        return prior_turns[-reference_window_turns:]

    def _resolve_explicit_references(
        self,
        query_turn: ConversationTurn,
        eligible_turns: tuple[ConversationTurn, ...],
        reference_ids: tuple[str, ...],
        matched_markers: tuple[str, ...],
    ) -> ConversationReferenceResolution:
        turns_by_identifier = {
            turn.turn_id: turn for turn in eligible_turns
        }
        candidate_turns: list[ConversationTurn] = []
        unresolved_ids: list[str] = []

        for reference_id in reference_ids:
            candidate = turns_by_identifier.get(reference_id)

            if candidate is None:
                unresolved_ids.append(reference_id)
                continue

            candidate_turns.append(candidate)

        if unresolved_ids:
            return ConversationReferenceResolution(
                state=(
                    ConversationReferenceResolutionState.UNRESOLVED
                ),
                query_turn_id=query_turn.turn_id,
                strategy="explicit_turn",
                matched_markers=matched_markers,
                candidate_turns=tuple(candidate_turns),
                unresolved_reference_ids=tuple(unresolved_ids),
            )

        return ConversationReferenceResolution(
            state=ConversationReferenceResolutionState.RESOLVED,
            query_turn_id=query_turn.turn_id,
            strategy="explicit_turn",
            matched_markers=matched_markers,
            candidate_turns=tuple(candidate_turns),
        )

    def _extract_explicit_reference_ids(
        self,
        content: str,
    ) -> tuple[str, ...]:
        identifiers: list[str] = []

        for identifier in self._EXPLICIT_TURN_PATTERN.findall(
            content
        ):
            if identifier not in identifiers:
                identifiers.append(identifier)

        return tuple(identifiers)

    def _find_implicit_markers(
        self,
        content: str,
    ) -> tuple[str, ...]:
        return tuple(
            marker
            for marker, pattern in self._IMPLICIT_MARKER_PATTERNS
            if pattern.search(content)
        )