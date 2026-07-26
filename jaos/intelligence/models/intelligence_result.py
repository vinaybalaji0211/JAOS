"""Core result model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.intelligence_result_status import (
    IntelligenceResultStatus,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize, validate, and deduplicate a tuple of strings."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{field_name} must contain only non-empty strings"
            )

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class IntelligenceResult:
    """Represents a validated result from an intelligence operation."""

    request_id: str
    status: IntelligenceResultStatus
    output: str | None = None
    result_id: str = field(default_factory=lambda: str(uuid4()))
    structured_output: dict[str, Any] = field(default_factory=dict)
    reasoning_summary: str | None = None
    assumptions: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    confidence: float = 0.0
    context_source_ids: tuple[str, ...] = ()
    provider_name: str | None = None
    provider_model: str | None = None
    proposed_actions: tuple[str, ...] = ()
    required_approvals: tuple[str, ...] = ()
    error_code: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize intelligence result invariants."""

        if not isinstance(self.result_id, str) or not self.result_id.strip():
            raise ValueError("result_id must be a non-empty string")

        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise ValueError("request_id must be a non-empty string")

        if not isinstance(self.status, IntelligenceResultStatus):
            raise TypeError(
                "status must be an instance of IntelligenceResultStatus"
            )

        if self.output is not None and not isinstance(self.output, str):
            raise TypeError("output must be a string or None")

        if self.reasoning_summary is not None and not isinstance(
            self.reasoning_summary,
            str,
        ):
            raise TypeError(
                "reasoning_summary must be a string or None"
            )

        if not isinstance(self.structured_output, dict):
            raise TypeError("structured_output must be a dictionary")

        if isinstance(self.confidence, bool) or not isinstance(
            self.confidence,
            (int, float),
        ):
            raise TypeError("confidence must be a number")

        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )

        optional_fields = {
            "provider_name": self.provider_name,
            "provider_model": self.provider_model,
            "error_code": self.error_code,
            "error_message": self.error_message,
        }

        for field_name, value in optional_fields.items():
            if value is not None and not isinstance(value, str):
                raise TypeError(
                    f"{field_name} must be a string or None"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.completed_at, datetime):
            raise TypeError("completed_at must be a datetime instance")

        if self.completed_at.tzinfo is None:
            raise ValueError("completed_at must be timezone-aware")

        output = self.output.strip() if self.output is not None else None
        reasoning_summary = (
            self.reasoning_summary.strip()
            if self.reasoning_summary is not None
            else None
        )
        provider_name = (
            self.provider_name.strip().lower()
            if self.provider_name is not None
            else None
        )
        provider_model = (
            self.provider_model.strip()
            if self.provider_model is not None
            else None
        )
        error_code = (
            self.error_code.strip().lower()
            if self.error_code is not None
            else None
        )
        error_message = (
            self.error_message.strip()
            if self.error_message is not None
            else None
        )

        if (
            self.status is IntelligenceResultStatus.SUCCEEDED
            and not output
            and not self.structured_output
        ):
            raise ValueError(
                "successful result must define output "
                "or structured_output"
            )

        if self.status in {
            IntelligenceResultStatus.FAILED,
            IntelligenceResultStatus.REJECTED,
        } and not error_message:
            raise ValueError(
                "failed or rejected result must define error_message"
            )

        object.__setattr__(self, "result_id", self.result_id.strip())
        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "output", output or None)
        object.__setattr__(
            self,
            "structured_output",
            dict(self.structured_output),
        )
        object.__setattr__(
            self,
            "reasoning_summary",
            reasoning_summary or None,
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
            "alternatives",
            _normalize_string_tuple(
                self.alternatives,
                "alternatives",
            ),
        )
        object.__setattr__(
            self,
            "risks",
            _normalize_string_tuple(self.risks, "risks"),
        )
        object.__setattr__(self, "confidence", float(self.confidence))
        object.__setattr__(
            self,
            "context_source_ids",
            _normalize_string_tuple(
                self.context_source_ids,
                "context_source_ids",
            ),
        )
        object.__setattr__(self, "provider_name", provider_name or None)
        object.__setattr__(self, "provider_model", provider_model or None)
        object.__setattr__(
            self,
            "proposed_actions",
            _normalize_string_tuple(
                self.proposed_actions,
                "proposed_actions",
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
        object.__setattr__(self, "error_code", error_code or None)
        object.__setattr__(self, "error_message", error_message or None)
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "status": self.status.value,
            "output": self.output,
            "structured_output": dict(self.structured_output),
            "reasoning_summary": self.reasoning_summary,
            "assumptions": list(self.assumptions),
            "alternatives": list(self.alternatives),
            "risks": list(self.risks),
            "confidence": self.confidence,
            "context_source_ids": list(self.context_source_ids),
            "provider_name": self.provider_name,
            "provider_model": self.provider_model,
            "proposed_actions": list(self.proposed_actions),
            "required_approvals": list(self.required_approvals),
            "error_code": self.error_code,
            "error_message": self.error_message,
            "metadata": dict(self.metadata),
            "completed_at": self.completed_at.isoformat(),
        }