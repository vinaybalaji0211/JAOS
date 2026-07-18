from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DiagnosticStatus:
    """
    Standard diagnostic result for AI Platform components.
    """

    component: str
    healthy: bool
    message: str
    details: dict[str, Any] = field(default_factory=dict)