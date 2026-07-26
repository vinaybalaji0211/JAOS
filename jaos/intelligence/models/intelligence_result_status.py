"""Result states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class IntelligenceResultStatus(str, Enum):
    """Describes the outcome of an intelligence request."""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED = "rejected"
    REQUIRES_CLARIFICATION = "requires_clarification"
    REQUIRES_APPROVAL = "requires_approval"