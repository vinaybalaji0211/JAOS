"""Decision status definitions for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class DecisionStatus(str, Enum):
    """Describes the lifecycle of a decision proposal."""

    DRAFT = "draft"
    VALIDATED = "validated"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
