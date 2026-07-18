from dataclasses import dataclass
from enum import Enum


class ToolApprovalLevel(str, Enum):
    NONE = "none"
    CONFIRMATION_REQUIRED = "confirmation_required"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"


class ToolApprovalError(Exception):
    """Raised when tool execution requires approval."""


@dataclass(frozen=True)
class ToolApprovalPolicy:
    level: ToolApprovalLevel = ToolApprovalLevel.NONE
    reason: str = ""

    def requires_approval(self) -> bool:
        return self.level != ToolApprovalLevel.NONE


class ToolApprovalManager:
    """
    Validates human approval requirements before tool execution.
    """

    def require_approval(
        self,
        policy: ToolApprovalPolicy,
        approved: bool,
    ) -> None:
        if policy.requires_approval() and not approved:
            reason = policy.reason or "Human approval is required."

            raise ToolApprovalError(reason)