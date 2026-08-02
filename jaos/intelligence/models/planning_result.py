"""Planning result model for the JAOS AI Intelligence Platform."""

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
class PlanningResult:
    """
    Represents the execution plan produced by the Planning Engine.
    """

    objective: str

    plan_summary: str

    execution_steps: tuple[str, ...] = ()

    dependencies: tuple[str, ...] = ()

    required_capabilities: tuple[str, ...] = ()

    constraints: tuple[str, ...] = ()

    assumptions: tuple[str, ...] = ()

    estimated_risks: tuple[str, ...] = ()

    estimated_duration_seconds: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    planning_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=_utc_now
    )

    def __post_init__(self) -> None:

        try:
            UUID(self.planning_id)
        except Exception as exc:
            raise ValueError(
                "planning_id must be a valid UUID"
            ) from exc

        if (
            not isinstance(self.objective, str)
            or not self.objective.strip()
        ):
            raise ValueError(
                "objective must be a non-empty string"
            )

        if (
            not isinstance(self.plan_summary, str)
            or not self.plan_summary.strip()
        ):
            raise ValueError(
                "plan_summary must be a non-empty string"
            )

        if self.estimated_duration_seconds is not None:
            if isinstance(
                self.estimated_duration_seconds,
                bool,
            ) or not isinstance(
                self.estimated_duration_seconds,
                (int, float),
            ):
                raise TypeError(
                    "estimated_duration_seconds "
                    "must be numeric"
                )

            if self.estimated_duration_seconds <= 0:
                raise ValueError(
                    "estimated_duration_seconds "
                    "must be greater than zero"
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
            "plan_summary",
            self.plan_summary.strip(),
        )

        object.__setattr__(
            self,
            "execution_steps",
            _normalize_string_tuple(
                self.execution_steps,
                "execution_steps",
            ),
        )

        object.__setattr__(
            self,
            "dependencies",
            _normalize_string_tuple(
                self.dependencies,
                "dependencies",
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
            "constraints",
            _normalize_string_tuple(
                self.constraints,
                "constraints",
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
            "estimated_risks",
            _normalize_string_tuple(
                self.estimated_risks,
                "estimated_risks",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

        if self.estimated_duration_seconds is not None:
            object.__setattr__(
                self,
                "estimated_duration_seconds",
                float(self.estimated_duration_seconds),
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent representation."""

        return {
            "planning_id": self.planning_id,
            "objective": self.objective,
            "plan_summary": self.plan_summary,
            "execution_steps": list(self.execution_steps),
            "dependencies": list(self.dependencies),
            "required_capabilities": list(
                self.required_capabilities
            ),
            "constraints": list(self.constraints),
            "assumptions": list(self.assumptions),
            "estimated_risks": list(
                self.estimated_risks
            ),
            "estimated_duration_seconds": (
                self.estimated_duration_seconds
            ),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }