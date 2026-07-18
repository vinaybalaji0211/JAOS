from dataclasses import dataclass
from enum import Enum


class AIProviderHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class AIProviderHealth:
    status: AIProviderHealthStatus
    message: str = ""