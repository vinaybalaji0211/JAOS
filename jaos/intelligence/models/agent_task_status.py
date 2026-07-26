"""Agent task states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class AgentTaskStatus(str, Enum):
    """Describes the lifecycle state of a structured agent task."""

    PENDING = "pending"
    ROUTED = "routed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"