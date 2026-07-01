from dataclasses import dataclass, field


@dataclass(slots=True)
class ServiceMetadata:
    """Metadata describing a registered JAOS service."""

    name: str
    version: str = "1.0.0"
    owner: str = "Unknown"
    status: str = "ACTIVE"
    dependencies: list[str] = field(default_factory=list)