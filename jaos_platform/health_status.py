from enum import Enum


class HealthStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    READY = "READY"
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"