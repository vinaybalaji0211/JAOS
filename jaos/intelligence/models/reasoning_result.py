"""Reasoning result model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.reasoning_assumption import (
    ReasoningAssumption,
)
from jaos.intelligence.models.risk_level import (
    RiskLevel,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize, validate and deduplicate tuples of strings."""

    if isinstance(values, (str, bytes)):
        raise TypeError(
            f"{field_name} must be a collection of strings"
        )

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if (
            not isinstance(item, str)
            or not item.strip()
        ):
            raise ValueError(
                f"{field_name} must contain only "
                "non-empty strings"
            )

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ReasoningResult:
    """
    Represents the validated output produced by the
    JAOS Reasoning Engine.
    """

    request_id: str

    objective_interpretation: str

    reasoning_summary: str

    confidence: float

    result_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    assumptions: tuple[
        ReasoningAssumption,
        ...
    ] = ()

    missing_information: tuple[str, ...] = ()

    alternatives: tuple[str, ...] = ()

    risks: tuple[str, ...] = ()

    constraints: tuple[str, ...] = ()

    risk_level: RiskLevel = RiskLevel.NONE

    recommended_next_action: str | None = None

    required_clarifications: tuple[str, ...] = ()

    required_approvals: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    completed_at: datetime = field(
        default_factory=_utc_now
    )
    def __post_init__(self) -> None:
        """Validate and normalize the reasoning result."""

        required_strings = {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "objective_interpretation": (
                self.objective_interpretation
            ),
            "reasoning_summary": (
                self.reasoning_summary
            ),
        }

        for field_name, value in required_strings.items():
            if (
                not isinstance(value, str)
                or not value.strip()
            ):
                raise ValueError(
                    f"{field_name} must be a "
                    "non-empty string"
                )

        if (
            isinstance(self.confidence, bool)
            or not isinstance(
                self.confidence,
                (int, float),
            )
        ):
            raise TypeError(
                "confidence must be a number"
            )

        confidence = float(self.confidence)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence must be between "
                "0.0 and 1.0"
            )

        assumptions = tuple(self.assumptions)

        seen_ids: set[str] = set()

        for assumption in assumptions:
            if not isinstance(
                assumption,
                ReasoningAssumption,
            ):
                raise TypeError(
                    "assumptions must contain only "
                    "ReasoningAssumption instances"
                )

            if (
                assumption.assumption_id
                in seen_ids
            ):
                raise ValueError(
                    "assumption IDs must be unique"
                )

            seen_ids.add(
                assumption.assumption_id
            )

        if not isinstance(
            self.risk_level,
            RiskLevel,
        ):
            raise TypeError(
                "risk_level must be an instance "
                "of RiskLevel"
            )

        if (
            self.recommended_next_action
            is not None
            and not isinstance(
                self.recommended_next_action,
                str,
            )
        ):
            raise TypeError(
                "recommended_next_action "
                "must be a string or None"
            )

        if not isinstance(
            self.metadata,
            dict,
        ):
            raise TypeError(
                "metadata must be a dictionary"
            )

        if not isinstance(
            self.completed_at,
            datetime,
        ):
            raise TypeError(
                "completed_at must be a "
                "datetime instance"
            )

        if self.completed_at.tzinfo is None:
            raise ValueError(
                "completed_at must be "
                "timezone-aware"
            )

        object.__setattr__(
            self,
            "request_id",
            self.request_id.strip(),
        )

        object.__setattr__(
            self,
            "result_id",
            self.result_id.strip(),
        )

        object.__setattr__(
            self,
            "objective_interpretation",
            self.objective_interpretation.strip(),
        )

        object.__setattr__(
            self,
            "reasoning_summary",
            self.reasoning_summary.strip(),
        )

        object.__setattr__(
            self,
            "confidence",
            confidence,
        )

        object.__setattr__(
            self,
            "assumptions",
            assumptions,
        )

        object.__setattr__(
            self,
            "missing_information",
            _normalize_string_tuple(
                self.missing_information,
                "missing_information",
            ),
        )

        object.__setattr__(
            self,
            "alternatives",
            _normalize_string_tuple(
                self.alternatives,
                "alternatives",
            ),
        )

        object.__setattr__(
            self,
            "risks",
            _normalize_string_tuple(
                self.risks,
                "risks",
            ),
        )

        object.__setattr__(
            self,
            "constraints",
            _normalize_string_tuple(
                self.constraints,
                "constraints",
            ),
        )

        object.__setattr__(
            self,
            "required_clarifications",
            _normalize_string_tuple(
                self.required_clarifications,
                "required_clarifications",
            ),
        )

        object.__setattr__(
            self,
            "required_approvals",
            _normalize_string_tuple(
                self.required_approvals,
                "required_approvals",
            ),
        )

        object.__setattr__(
            self,
            "recommended_next_action",
            (
                self.recommended_next_action.strip()
                if self.recommended_next_action
                else None
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )
    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary."""

        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "objective_interpretation": (
                self.objective_interpretation
            ),
            "reasoning_summary": (
                self.reasoning_summary
            ),
            "confidence": self.confidence,
            "assumptions": [
                assumption.to_dict()
                for assumption in self.assumptions
            ],
            "missing_information": list(
                self.missing_information
            ),
            "alternatives": list(
                self.alternatives
            ),
            "risks": list(self.risks),
            "constraints": list(
                self.constraints
            ),
            "risk_level": self.risk_level.value,
            "recommended_next_action": (
                self.recommended_next_action
            ),
            "required_clarifications": list(
                self.required_clarifications
            ),
            "required_approvals": list(
                self.required_approvals
            ),
            "metadata": dict(self.metadata),
            "completed_at": (
                self.completed_at.isoformat()
            ),
        }