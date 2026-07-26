"""Agent health states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class AgentHealthState(str, Enum):
    """Describes the operational health of an intelligence agent."""

    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"