"""Agent availability states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class AgentAvailabilityState(str, Enum):
    """Describes whether an intelligence agent can accept a task."""

    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"