"""Canonical legal-transition table and validator for RuntimeLifecycleState."""

from __future__ import annotations

from typing import Final, FrozenSet, Mapping

from jaos_platform.lifecycle_state import RuntimeLifecycleState


class LifecycleTransitionError(ValueError):
    """Raised when a RuntimeLifecycleState transition is not legal."""


_S = RuntimeLifecycleState

LIFECYCLE_TRANSITIONS: Final[Mapping[RuntimeLifecycleState, FrozenSet[RuntimeLifecycleState]]] = {
    _S.CREATED: frozenset({_S.INITIALIZING}),
    _S.INITIALIZING: frozenset({_S.INITIALIZED, _S.FAILED}),
    _S.INITIALIZED: frozenset({_S.STARTING, _S.STOPPING}),
    _S.STARTING: frozenset({_S.READY, _S.DEGRADED, _S.ROLLING_BACK, _S.FAILED}),
    _S.READY: frozenset({_S.DEGRADED, _S.STOPPING, _S.FAILED}),
    _S.DEGRADED: frozenset({_S.READY, _S.STOPPING, _S.FAILED}),
    _S.ROLLING_BACK: frozenset({_S.STOPPED, _S.FAILED}),
    _S.STOPPING: frozenset({_S.STOPPED, _S.FAILED}),
    _S.STOPPED: frozenset(),
    _S.FAILED: frozenset(),
}


def validate_transition(
    current: RuntimeLifecycleState, target: RuntimeLifecycleState
) -> RuntimeLifecycleState:
    """Return target if current -> target is legal; raise LifecycleTransitionError otherwise."""
    if not isinstance(current, RuntimeLifecycleState):
        raise LifecycleTransitionError(
            f"current must be a RuntimeLifecycleState, got {current!r}"
        )
    if not isinstance(target, RuntimeLifecycleState):
        raise LifecycleTransitionError(
            f"target must be a RuntimeLifecycleState, got {target!r}"
        )

    legal_targets = LIFECYCLE_TRANSITIONS[current]
    if target not in legal_targets:
        raise LifecycleTransitionError(
            f"illegal lifecycle transition: {current.value} -> {target.value}"
        )

    return target
