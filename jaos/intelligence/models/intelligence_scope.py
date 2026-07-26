"""Identity scopes for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class IntelligenceScope(str, Enum):
    """Defines the ownership and permission scope of intelligence data."""

    GLOBAL = "global"
    SYSTEM = "system"
    USER = "user"
    DEVICE = "device"
    SESSION = "session"
    MISSION = "mission"
    PROJECT = "project"
    AGENT = "agent"