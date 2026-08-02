"""Validation states for intelligence context."""

from enum import Enum


class ContextValidationState(str, Enum):
    """Represents validation status of contextual information."""

    UNKNOWN = "unknown"
    VALID = "valid"
    INVALID = "invalid"
    PARTIALLY_VALID = "partially_valid"
    CONFLICTING = "conflicting"