"""Decision confidence definitions for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class DecisionConfidence(str, Enum):
    """
    Defines the confidence level assigned to a
    decision proposal.

    Decision confidence represents how strongly
    the Decision Engine believes the selected
    decision is appropriate based on the available
    information.
    """

    LOW = "low"
    """The decision has significant uncertainty."""

    MEDIUM = "medium"
    """The decision is reasonable but contains some uncertainty."""

    HIGH = "high"
    """The decision is well supported by the available information."""

    VERY_HIGH = "very_high"
    """The decision has extremely high confidence and minimal uncertainty."""
