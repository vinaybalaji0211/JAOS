"""Agent descriptor model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from typing import Any

from jaos.intelligence.models.agent_availability_state import (
    AgentAvailabilityState,
)
from jaos.intelligence.models.agent_health_state import AgentHealthState


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of identifiers."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{field_name} must contain only non-empty strings"
            )

        value = item.strip().lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class AgentDescriptor:
    """Describes a controlled intelligence agent and its capabilities."""

    agent_id: str
    name: str
    capabilities: tuple[str, ...]
    input_contracts: tuple[str, ...]
    output_contracts: tuple[str, ...]
    required_permissions: tuple[str, ...] = ()
    availability_state: AgentAvailabilityState = (
        AgentAvailabilityState.AVAILABLE
    )
    health_state: AgentHealthState = AgentHealthState.UNKNOWN
    max_delegation_depth: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize agent-descriptor invariants."""

        required_strings = {
            "agent_id": self.agent_id,
            "name": self.name,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        capabilities = _normalize_string_tuple(
            self.capabilities,
            "capabilities",
        )
        input_contracts = _normalize_string_tuple(
            self.input_contracts,
            "input_contracts",
        )
        output_contracts = _normalize_string_tuple(
            self.output_contracts,
            "output_contracts",
        )

        if not capabilities:
            raise ValueError(
                "capabilities must contain at least one value"
            )

        if not input_contracts:
            raise ValueError(
                "input_contracts must contain at least one value"
            )

        if not output_contracts:
            raise ValueError(
                "output_contracts must contain at least one value"
            )

        if not isinstance(
            self.availability_state,
            AgentAvailabilityState,
        ):
            raise TypeError(
                "availability_state must be an instance of "
                "AgentAvailabilityState"
            )

        if not isinstance(self.health_state, AgentHealthState):
            raise TypeError(
                "health_state must be an instance of AgentHealthState"
            )

        if isinstance(self.max_delegation_depth, bool) or not isinstance(
            self.max_delegation_depth,
            int,
        ):
            raise TypeError(
                "max_delegation_depth must be an integer"
            )

        if self.max_delegation_depth < 0:
            raise ValueError(
                "max_delegation_depth cannot be negative"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        object.__setattr__(
            self,
            "agent_id",
            self.agent_id.strip().lower(),
        )
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "capabilities", capabilities)
        object.__setattr__(
            self,
            "input_contracts",
            input_contracts,
        )
        object.__setattr__(
            self,
            "output_contracts",
            output_contracts,
        )
        object.__setattr__(
            self,
            "required_permissions",
            _normalize_string_tuple(
                self.required_permissions,
                "required_permissions",
            ),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": list(self.capabilities),
            "input_contracts": list(self.input_contracts),
            "output_contracts": list(self.output_contracts),
            "required_permissions": list(
                self.required_permissions
            ),
            "availability_state": self.availability_state.value,
            "health_state": self.health_state.value,
            "max_delegation_depth": self.max_delegation_depth,
            "metadata": dict(self.metadata),
        }