"""Confidence assessment model for the JAOS AI Intelligence Platform."""

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
class ConfidenceAssessment:
    """
    Represents a structured confidence evaluation for an
    intelligence operation.
    """

    overall_confidence: float

    confidence_summary: str

    confidence_factors: tuple[str, ...] = ()

    uncertainty_sources: tuple[str, ...] = ()

    supporting_evidence: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(default_factory=dict)

    assessment_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=_utc_now
    )

    def __post_init__(self) -> None:

        try:
            UUID(self.assessment_id)
        except Exception as exc:
            raise ValueError(
                "assessment_id must be a valid UUID"
            ) from exc

        if isinstance(
            self.overall_confidence,
            bool,
        ) or not isinstance(
            self.overall_confidence,
            (int, float),
        ):
            raise TypeError(
                "overall_confidence must be numeric"
            )

        confidence = float(self.overall_confidence)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "overall_confidence must be between "
                "0.0 and 1.0"
            )

        if (
            not isinstance(
                self.confidence_summary,
                str,
            )
            or not self.confidence_summary.strip()
        ):
            raise ValueError(
                "confidence_summary must be a "
                "non-empty string"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError(
                "metadata must be a dictionary"
            )

        if not isinstance(
            self.created_at,
            datetime,
        ):
            raise TypeError(
                "created_at must be datetime"
            )

        if self.created_at.tzinfo is None:
            raise ValueError(
                "created_at must be timezone-aware"
            )

        object.__setattr__(
            self,
            "overall_confidence",
            confidence,
        )

        object.__setattr__(
            self,
            "confidence_summary",
            self.confidence_summary.strip(),
        )

        object.__setattr__(
            self,
            "confidence_factors",
            _normalize_string_tuple(
                self.confidence_factors,
                "confidence_factors",
            ),
        )

        object.__setattr__(
            self,
            "uncertainty_sources",
            _normalize_string_tuple(
                self.uncertainty_sources,
                "uncertainty_sources",
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
            "metadata",
            dict(self.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent representation."""

        return {
            "assessment_id": self.assessment_id,
            "overall_confidence": self.overall_confidence,
            "confidence_summary": self.confidence_summary,
            "confidence_factors": list(
                self.confidence_factors
            ),
            "uncertainty_sources": list(
                self.uncertainty_sources
            ),
            "supporting_evidence": list(
                self.supporting_evidence
            ),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }