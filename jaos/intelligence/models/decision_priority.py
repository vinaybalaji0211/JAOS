"""Decision priority definitions for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class DecisionPriority(str, Enum):
    """
    Defines the execution priority assigned to a
    decision proposal.

    Decision priority influences scheduling and
    execution ordering after a decision has been
    approved. It does not affect planning,
    reasoning, or policy evaluation.
    """

    LOW = "low"
    """Background or deferrable decisions."""

    NORMAL = "normal"
    """Standard execution priority."""

    HIGH = "high"
    """Time-sensitive decisions requiring prompt execution."""

    CRITICAL = "critical"
    """Highest execution priority for critical system or safety operations."""
