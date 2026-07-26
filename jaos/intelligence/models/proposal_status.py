"""Proposal states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class ProposalStatus(str, Enum):
    """Describes the lifecycle of a plan or execution proposal."""

    DRAFT = "draft"
    VALIDATED = "validated"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"