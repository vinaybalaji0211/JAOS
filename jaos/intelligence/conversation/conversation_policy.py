"""Conversation runtime policy for the JAOS Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _normalize_required_text(
    value: str,
    field_name: str,
) -> str:
    """Validate and normalize a required policy string."""

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip().lower()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


def _validate_positive_integer(
    value: int,
    field_name: str,
) -> int:
    """Validate a strictly positive integer."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero"
        )

    return value


@dataclass(frozen=True, slots=True)
class ConversationPolicy:
    """
    Defines approved behavior for one conversation runtime mode.

    Enabling memory-candidate submission permits only structured candidate
    handoff. It never authorizes direct creation of permanent memory.
    """

    policy_name: str = "default"
    context_policy: str = "default"
    max_history_turns: int = 100
    reference_window_turns: int = 20
    allow_reference_resolution: bool = True
    allow_interruption: bool = True
    allow_continuation: bool = True
    require_context_bundle: bool = True
    working_memory_enabled: bool = True
    memory_candidate_submission_enabled: bool = False
    max_provider_response_characters: int = 50_000
    max_provider_metadata_items: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize policy invariants."""

        policy_name = _normalize_required_text(
            self.policy_name,
            "policy_name",
        )
        context_policy = _normalize_required_text(
            self.context_policy,
            "context_policy",
        )

        max_history_turns = _validate_positive_integer(
            self.max_history_turns,
            "max_history_turns",
        )
        reference_window_turns = _validate_positive_integer(
            self.reference_window_turns,
            "reference_window_turns",
        )
        max_provider_response_characters = (
            _validate_positive_integer(
                self.max_provider_response_characters,
                "max_provider_response_characters",
            )
        )
        max_provider_metadata_items = _validate_positive_integer(
            self.max_provider_metadata_items,
            "max_provider_metadata_items",
        )

        if reference_window_turns > max_history_turns:
            raise ValueError(
                "reference_window_turns must not exceed "
                "max_history_turns"
            )

        boolean_fields = {
            "allow_reference_resolution": (
                self.allow_reference_resolution
            ),
            "allow_interruption": self.allow_interruption,
            "allow_continuation": self.allow_continuation,
            "require_context_bundle": self.require_context_bundle,
            "working_memory_enabled": self.working_memory_enabled,
            "memory_candidate_submission_enabled": (
                self.memory_candidate_submission_enabled
            ),
        }

        for field_name, value in boolean_fields.items():
            if not isinstance(value, bool):
                raise TypeError(
                    f"{field_name} must be a boolean"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        object.__setattr__(self, "policy_name", policy_name)
        object.__setattr__(self, "context_policy", context_policy)
        object.__setattr__(
            self,
            "max_history_turns",
            max_history_turns,
        )
        object.__setattr__(
            self,
            "reference_window_turns",
            reference_window_turns,
        )
        object.__setattr__(
            self,
            "max_provider_response_characters",
            max_provider_response_characters,
        )
        object.__setattr__(
            self,
            "max_provider_metadata_items",
            max_provider_metadata_items,
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-friendly policy representation."""

        return {
            "policy_name": self.policy_name,
            "context_policy": self.context_policy,
            "max_history_turns": self.max_history_turns,
            "reference_window_turns": (
                self.reference_window_turns
            ),
            "allow_reference_resolution": (
                self.allow_reference_resolution
            ),
            "allow_interruption": self.allow_interruption,
            "allow_continuation": self.allow_continuation,
            "require_context_bundle": self.require_context_bundle,
            "working_memory_enabled": self.working_memory_enabled,
            "memory_candidate_submission_enabled": (
                self.memory_candidate_submission_enabled
            ),
            "max_provider_response_characters": (
                self.max_provider_response_characters
            ),
            "max_provider_metadata_items": (
                self.max_provider_metadata_items
            ),
            "metadata": dict(self.metadata),
        }