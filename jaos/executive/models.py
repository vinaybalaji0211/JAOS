from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ExecutiveIntentType(str, Enum):
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    COPY_FILE = "copy_file"
    MOVE_FILE = "move_file"
    RENAME_FILE = "rename_file"
    DELETE_FILE = "delete_file"
    SEARCH_FILE = "search_file"
    BACKUP_FILE = "backup_file"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ExecutiveIntent:
    intent_type: ExecutiveIntentType
    confidence: float
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutivePlanStep:
    tool_name: str
    payload: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False
    approved: bool = True


@dataclass(frozen=True)
class ExecutivePlan:
    intent: ExecutiveIntent
    steps: tuple[ExecutivePlanStep, ...] = ()


@dataclass(frozen=True)
class ExecutiveResponse:
    success: bool
    message: str
    output: Any = None