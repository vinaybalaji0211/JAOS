"""Proposed plan-step model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.failure_behavior import (
    FailureBehavior,
)
from jaos.intelligence.models.risk_level import RiskLevel


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    lowercase: bool = False,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of non-empty strings."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(f"{field_name} must be a collection of strings") from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings")

        value = item.strip()

        if lowercase:
            value = value.lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ProposedPlanStep:
    """Represents one non-authoritative step in a plan proposal."""

    description: str
    step_order: int
    required_capability: str
    expected_output: str
    success_condition: str
    step_id: str = field(default_factory=lambda: str(uuid4()))
    dependencies: tuple[str, ...] = ()
    suggested_tool_category: str | None = None
    input_references: tuple[str, ...] = ()
    permission_requirements: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.NONE
    failure_behavior: FailureBehavior = FailureBehavior.STOP
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize proposed-step invariants."""

        required_strings = {
            "step_id": self.step_id,
            "description": self.description,
            "required_capability": self.required_capability,
            "expected_output": self.expected_output,
            "success_condition": self.success_condition,
            "failure_behavior": self.failure_behavior,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if isinstance(self.step_order, bool) or not isinstance(
            self.step_order,
            int,
        ):
            raise TypeError("step_order must be an integer")

        if self.step_order <= 0:
            raise ValueError("step_order must be greater than zero")

        if self.suggested_tool_category is not None and not isinstance(
            self.suggested_tool_category, str
        ):
            raise TypeError("suggested_tool_category must be a string or None")

        if not isinstance(self.risk_level, RiskLevel):
            raise TypeError("risk_level must be an instance of RiskLevel")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        step_id = self.step_id.strip()
        dependencies = _normalize_string_tuple(
            self.dependencies,
            "dependencies",
        )

        if step_id in dependencies:
            raise ValueError("a proposed plan step cannot depend on itself")

        suggested_tool_category = (
            self.suggested_tool_category.strip().lower()
            if self.suggested_tool_category is not None
            else None
        )

        object.__setattr__(self, "step_id", step_id)
        object.__setattr__(
            self,
            "description",
            self.description.strip(),
        )
        object.__setattr__(
            self,
            "required_capability",
            self.required_capability.strip().lower(),
        )
        object.__setattr__(
            self,
            "expected_output",
            self.expected_output.strip(),
        )
        object.__setattr__(
            self,
            "success_condition",
            self.success_condition.strip(),
        )
        object.__setattr__(self, "dependencies", dependencies)
        object.__setattr__(
            self,
            "suggested_tool_category",
            suggested_tool_category or None,
        )
        object.__setattr__(
            self,
            "input_references",
            _normalize_string_tuple(
                self.input_references,
                "input_references",
            ),
        )
        object.__setattr__(
            self,
            "permission_requirements",
            _normalize_string_tuple(
                self.permission_requirements,
                "permission_requirements",
                lowercase=True,
            ),
        )
        object.__setattr__(
            self,
            "failure_behavior",
            self.failure_behavior.strip().lower(),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "step_id": self.step_id,
            "description": self.description,
            "step_order": self.step_order,
            "dependencies": list(self.dependencies),
            "required_capability": self.required_capability,
            "suggested_tool_category": self.suggested_tool_category,
            "input_references": list(self.input_references),
            "expected_output": self.expected_output,
            "permission_requirements": list(self.permission_requirements),
            "risk_level": self.risk_level.value,
            "success_condition": self.success_condition,
            "failure_behavior": self.failure_behavior,
            "metadata": dict(self.metadata),
        }
