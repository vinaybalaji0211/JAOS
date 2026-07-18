from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DiagnosticStatus:
    """
    Standard diagnostic result for Executive components.
    """

    component: str
    healthy: bool
    message: str
    details: dict[str, Any]