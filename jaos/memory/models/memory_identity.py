"""Memory identity model for the JAOS Memory Platform."""

from dataclasses import dataclass

from jaos.memory.models.memory_scope import MemoryScope


@dataclass(frozen=True, slots=True)
class MemoryIdentity:
    """Associates a memory with an approved visibility scope and identifier."""

    scope: MemoryScope
    identity_id: str | None = None

    def __post_init__(self) -> None:
        """Validate identity invariants."""

        if not isinstance(self.scope, MemoryScope):
            raise TypeError("scope must be an instance of MemoryScope")

        if self.scope is MemoryScope.GLOBAL:
            if self.identity_id is not None:
                raise ValueError(
                    "global memory identity must not define identity_id"
                )
            return

        if not isinstance(self.identity_id, str) or not self.identity_id.strip():
            raise ValueError(
                "identity_id must be a non-empty string for non-global scopes"
            )

        object.__setattr__(self, "identity_id", self.identity_id.strip())