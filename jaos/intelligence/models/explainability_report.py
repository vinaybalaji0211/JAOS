"""Explainability report model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize and validate tuples of strings."""

    if isinstance(values, (str, bytes)):
        raise TypeError(
            f"{field_name} must be a collection of strings"
        )

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be iterable"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str):
            raise TypeError(
                f"{field_name} must contain strings"
            )

        value = item.strip()

        if not value:
            raise ValueError(
                f"{field_name} cannot contain empty strings"
            )

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ExplainabilityReport:
    """
    Represents a structured explanation describing how an
    intelligence decision was produced.
    """

    objective: str

    explanation_summary: str

    reasoning_trace: tuple[str, ...] = ()

    planning_trace: tuple[str, ...] = ()

    decision_trace: tuple[str, ...] = ()

    supporting_evidence: tuple[str, ...] = ()

    assumptions: tuple[str, ...] = ()

    alternatives_considered: tuple[str, ...] = ()

    identified_risks: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(default_factory=dict)

    report_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=_utc_now
    )

    def __post_init__(self) -> None:

        try:
            UUID(self.report_id)
        except Exception as exc:
            raise ValueError(
                "report_id must be a valid UUID"
            ) from exc

        required_strings = {
            "objective": self.objective,
            "explanation_summary": self.explanation_summary,
        }

        for field_name, value in required_strings.items():
            if (
                not isinstance(value, str)
                or not value.strip()
            ):
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError(
                "metadata must be a dictionary"
            )

        if not isinstance(self.created_at, datetime):
            raise TypeError(
                "created_at must be datetime"
            )

        if self.created_at.tzinfo is None:
            raise ValueError(
                "created_at must be timezone-aware"
            )

        object.__setattr__(
            self,
            "objective",
            self.objective.strip(),
        )

        object.__setattr__(
            self,
            "explanation_summary",
            self.explanation_summary.strip(),
        )

        object.__setattr__(
            self,
            "reasoning_trace",
            _normalize_string_tuple(
                self.reasoning_trace,
                "reasoning_trace",
            ),
        )

        object.__setattr__(
            self,
            "planning_trace",
            _normalize_string_tuple(
                self.planning_trace,
                "planning_trace",
            ),
        )

        object.__setattr__(
            self,
            "decision_trace",
            _normalize_string_tuple(
                self.decision_trace,
                "decision_trace",
            ),
        )

        object.__setattr__(
            self,
            "supporting_evidence",
            _normalize_string_tuple(
                self.supporting_evidence,
                "supporting_evidence",
            ),
        )

        object.__setattr__(
            self,
            "assumptions",
            _normalize_string_tuple(
                self.assumptions,
                "assumptions",
            ),
        )

        object.__setattr__(
            self,
            "alternatives_considered",
            _normalize_string_tuple(
                self.alternatives_considered,
                "alternatives_considered",
            ),
        )

        object.__setattr__(
            self,
            "identified_risks",
            _normalize_string_tuple(
                self.identified_risks,
                "identified_risks",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent representation."""

        return {
            "report_id": self.report_id,
            "objective": self.objective,
            "explanation_summary": self.explanation_summary,
            "reasoning_trace": list(self.reasoning_trace),
            "planning_trace": list(self.planning_trace),
            "decision_trace": list(self.decision_trace),
            "supporting_evidence": list(self.supporting_evidence),
            "assumptions": list(self.assumptions),
            "alternatives_considered": list(
                self.alternatives_considered
            ),
            "identified_risks": list(
                self.identified_risks
            ),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }