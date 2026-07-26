"""Versioned prompt templates for the JAOS Intelligence Platform."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from jaos.ai.provider.provider_config import AIProviderCapability


_VERSION_PATTERN = re.compile(
    r"^\d+(?:\.\d+){1,2}(?:[-+][A-Za-z0-9.-]+)?$"
)


def _normalize_required_text(
    value: str,
    field_name: str,
) -> str:
    """Validate and normalize required text."""

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


def _normalize_capabilities(
    capabilities: tuple[AIProviderCapability | str, ...],
) -> tuple[AIProviderCapability, ...]:
    """Normalize and deduplicate provider capabilities."""

    if not isinstance(capabilities, tuple):
        raise TypeError(
            "required_provider_capabilities must be a tuple"
        )

    normalized_capabilities: list[AIProviderCapability] = []

    for capability in capabilities:
        if isinstance(capability, AIProviderCapability):
            normalized = capability
        elif isinstance(capability, str):
            try:
                normalized = AIProviderCapability(
                    capability.strip().lower()
                )
            except ValueError as exc:
                raise ValueError(
                    f"unsupported provider capability: {capability}"
                ) from exc
        else:
            raise TypeError(
                "provider capabilities must be "
                "AIProviderCapability instances or strings"
            )

        if normalized not in normalized_capabilities:
            normalized_capabilities.append(normalized)

    if not normalized_capabilities:
        raise ValueError(
            "required_provider_capabilities must not be empty"
        )

    return tuple(normalized_capabilities)


def _validate_json_mapping(
    value: dict[str, Any],
    field_name: str,
) -> dict[str, Any]:
    """Validate a JSON-serializable dictionary."""

    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dictionary")

    if not all(isinstance(key, str) for key in value):
        raise TypeError(f"{field_name} keys must be strings")

    try:
        json.dumps(value, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{field_name} must be JSON serializable"
        ) from exc

    return dict(value)


@dataclass(frozen=True, slots=True)
class IntelligencePromptTemplate:
    """Approved, versioned instructions for prompt composition."""

    template_id: str
    version: str
    system_instruction: str
    task_instruction: str
    required_provider_capabilities: tuple[
        AIProviderCapability | str,
        ...,
    ] = (AIProviderCapability.CHAT,)
    default_output_schema: dict[str, Any] = field(
        default_factory=dict
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize template invariants."""

        template_id = _normalize_required_text(
            self.template_id,
            "template_id",
        ).lower()
        version = _normalize_required_text(
            self.version,
            "version",
        )

        if not _VERSION_PATTERN.fullmatch(version):
            raise ValueError(
                "version must be a dotted version such as "
                "1.0 or 1.0.0"
            )

        object.__setattr__(self, "template_id", template_id)
        object.__setattr__(self, "version", version)
        object.__setattr__(
            self,
            "system_instruction",
            _normalize_required_text(
                self.system_instruction,
                "system_instruction",
            ),
        )
        object.__setattr__(
            self,
            "task_instruction",
            _normalize_required_text(
                self.task_instruction,
                "task_instruction",
            ),
        )
        object.__setattr__(
            self,
            "required_provider_capabilities",
            _normalize_capabilities(
                self.required_provider_capabilities
            ),
        )
        object.__setattr__(
            self,
            "default_output_schema",
            _validate_json_mapping(
                self.default_output_schema,
                "default_output_schema",
            ),
        )
        object.__setattr__(
            self,
            "metadata",
            _validate_json_mapping(
                self.metadata,
                "metadata",
            ),
        )

    @property
    def reference(self) -> str:
        """Return the stable template reference."""

        return f"{self.template_id}@{self.version}"

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe template representation."""

        return {
            "template_id": self.template_id,
            "version": self.version,
            "reference": self.reference,
            "system_instruction": self.system_instruction,
            "task_instruction": self.task_instruction,
            "required_provider_capabilities": [
                capability.value
                for capability
                in self.required_provider_capabilities
            ],
            "default_output_schema": dict(
                self.default_output_schema
            ),
            "metadata": dict(self.metadata),
        }