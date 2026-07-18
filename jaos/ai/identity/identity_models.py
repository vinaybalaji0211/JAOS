from dataclasses import dataclass, field


@dataclass(frozen=True)
class JAOSCapability:
    """
    Represents a capability currently available to JAOS.
    """

    name: str
    description: str


@dataclass(frozen=True)
class JAOSLimitation:
    """
    Represents an operational limitation of JAOS.
    """

    name: str
    description: str


@dataclass(frozen=True)
class JAOSIdentity:
    """
    Canonical identity of the running JAOS instance.
    """

    name: str
    version: str
    codename: str
    description: str

    capabilities: tuple[JAOSCapability, ...] = field(default_factory=tuple)
    limitations: tuple[JAOSLimitation, ...] = field(default_factory=tuple)