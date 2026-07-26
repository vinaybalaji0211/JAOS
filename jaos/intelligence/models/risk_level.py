"""Risk levels for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class RiskLevel(str, Enum):
    """Classifies the risk associated with a proposed operation."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"