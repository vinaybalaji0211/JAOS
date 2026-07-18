from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from jaos.tools.tool_approval import ToolApprovalPolicy
from jaos.tools.tool_capabilities import ToolCapability


class ToolRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ToolStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DISABLED = "disabled"


@dataclass(frozen=True)
class ToolMetadata:
    name: str
    version: str
    description: str
    permissions: tuple[str, ...] = ()
    capabilities: tuple[ToolCapability, ...] = ()
    approval_policy: ToolApprovalPolicy = field(default_factory=ToolApprovalPolicy)
    risk_level: ToolRiskLevel = ToolRiskLevel.LOW
    status: ToolStatus = ToolStatus.AVAILABLE

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Tool name cannot be empty")
        if not self.version.strip():
            raise ValueError("Tool version cannot be empty")
        if not self.description.strip():
            raise ValueError("Tool description cannot be empty")


@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    payload: dict[str, Any] = field(default_factory=dict)
    approved: bool = False

    def __post_init__(self) -> None:
        if not self.tool_name.strip():
            raise ValueError("Tool name cannot be empty")


@dataclass(frozen=True)
class ToolResult:
    success: bool
    output: Any = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))