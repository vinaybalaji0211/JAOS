"""Decision result model for the JAOS AI Intelligence Platform."""

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
class DecisionResult:
    """
    Represents the final decision produced by the Decision Engine.
    """

    objective: str

    selected_strategy: str

    decision_summary: str

    rationale: str

    recommended_actions: tuple[str, ...] = ()

    rejected_alternatives: tuple[str, ...] = ()

    identified_risks: tuple[str, ...] = ()

    required_approvals: tuple[str, ...] = ()

    required_capabilities: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(default_factory=dict)

    decision_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=_utc_now
    )

    def __post_init__(self) -> None:

        try:
            UUID(self.decision_id)
        except Exception as exc:
            raise ValueError(
                "decision_id must be a valid UUID"
            ) from exc

        required_strings = {
            "objective": self.objective,
            "selected_strategy": self.selected_strategy,
            "decision_summary": self.decision_summary,
            "rationale": self.rationale,
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
            "selected_strategy",
            self.selected_strategy.strip(),
        )

        object.__setattr__(
            self,
            "decision_summary",
            self.decision_summary.strip(),
        )

        object.__setattr__(
            self,
            "rationale",
            self.rationale.strip(),
        )

        object.__setattr__(
            self,
            "recommended_actions",
            _normalize_string_tuple(
                self.recommended_actions,
                "recommended_actions",
            ),
        )

        object.__setattr__(
            self,
            "rejected_alternatives",
            _normalize_string_tuple(
                self.rejected_alternatives,
                "rejected_alternatives",
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
            "required_approvals",
            _normalize_string_tuple(
                self.required_approvals,
                "required_approvals",
            ),
        )

        object.__setattr__(
            self,
            "required_capabilities",
            _normalize_string_tuple(
                self.required_capabilities,
                "required_capabilities",
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
            "decision_id": self.decision_id,
            "objective": self.objective,
            "selected_strategy": self.selected_strategy,
            "decision_summary": self.decision_summary,
            "rationale": self.rationale,
            "recommended_actions": list(
                self.recommended_actions
            ),
            "rejected_alternatives": list(
                self.rejected_alternatives
            ),
            "identified_risks": list(
                self.identified_risks
            ),
            "required_approvals": list(
                self.required_approvals
            ),
            "required_capabilities": list(
                self.required_capabilities
            ),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }