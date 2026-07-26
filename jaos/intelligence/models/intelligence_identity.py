"""Identity model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass
from typing import Any

from jaos.intelligence.models.intelligence_scope import IntelligenceScope


@dataclass(frozen=True, slots=True)
class IntelligenceIdentity:
    """Associates intelligence data with an approved ownership scope."""

    scope: IntelligenceScope
    identity_id: str | None = None

    def __post_init__(self) -> None:
        """Validate and normalize identity invariants."""

        if not isinstance(self.scope, IntelligenceScope):
            raise TypeError(
                "scope must be an instance of IntelligenceScope"
            )

        if self.scope is IntelligenceScope.GLOBAL:
            if self.identity_id is not None:
                raise ValueError(
                    "global intelligence identity must not define identity_id"
                )
            return

        if (
            not isinstance(self.identity_id, str)
            or not self.identity_id.strip()
        ):
            raise ValueError(
                "identity_id must be a non-empty string "
                "for non-global scopes"
            )

        object.__setattr__(self, "identity_id", self.identity_id.strip())

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "scope": self.scope.value,
            "identity_id": self.identity_id,
        }