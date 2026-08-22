import os

import pytest

from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.lifecycle_transitions import (
    LIFECYCLE_TRANSITIONS,
    LifecycleTransitionError,
    validate_transition,
)

_S = RuntimeLifecycleState

_LEGAL_PAIRS = [
    (current, target)
    for current, targets in LIFECYCLE_TRANSITIONS.items()
    for target in targets
]

_ILLEGAL_PAIRS = [
    (_S.CREATED, _S.READY),
    (_S.CREATED, _S.STARTING),
    (_S.READY, _S.CREATED),
    (_S.INITIALIZED, _S.READY),
    (_S.STARTING, _S.STOPPED),
    (_S.STOPPED, _S.CREATED),
    (_S.STOPPED, _S.READY),
    (_S.FAILED, _S.CREATED),
    (_S.FAILED, _S.READY),
    (_S.DEGRADED, _S.STARTING),
    (_S.ROLLING_BACK, _S.READY),
    (_S.ROLLING_BACK, _S.STARTING),
]


def test_enum_completeness():
    assert {member.name for member in RuntimeLifecycleState} == {
        "CREATED",
        "INITIALIZING",
        "INITIALIZED",
        "STARTING",
        "READY",
        "DEGRADED",
        "STOPPING",
        "STOPPED",
        "ROLLING_BACK",
        "FAILED",
    }


def test_enum_values_match_names():
    for member in RuntimeLifecycleState:
        assert member.value == member.name


def test_transition_table_covers_every_state():
    assert set(LIFECYCLE_TRANSITIONS.keys()) == set(RuntimeLifecycleState)


@pytest.mark.parametrize("current,target", _LEGAL_PAIRS)
def test_every_legal_transition_is_accepted(current, target):
    assert validate_transition(current, target) is target


@pytest.mark.parametrize("current,target", _ILLEGAL_PAIRS)
def test_representative_illegal_transitions_are_rejected(current, target):
    with pytest.raises(LifecycleTransitionError):
        validate_transition(current, target)


def test_stopped_is_terminal():
    assert LIFECYCLE_TRANSITIONS[_S.STOPPED] == frozenset()
    for target in RuntimeLifecycleState:
        with pytest.raises(LifecycleTransitionError):
            validate_transition(_S.STOPPED, target)


def test_failed_is_terminal():
    assert LIFECYCLE_TRANSITIONS[_S.FAILED] == frozenset()
    for target in RuntimeLifecycleState:
        with pytest.raises(LifecycleTransitionError):
            validate_transition(_S.FAILED, target)


def test_ready_and_degraded_are_mutually_reachable():
    assert validate_transition(_S.READY, _S.DEGRADED) is _S.DEGRADED
    assert validate_transition(_S.DEGRADED, _S.READY) is _S.READY


def test_rollback_transitions():
    assert validate_transition(_S.STARTING, _S.ROLLING_BACK) is _S.ROLLING_BACK
    assert validate_transition(_S.ROLLING_BACK, _S.STOPPED) is _S.STOPPED
    assert validate_transition(_S.ROLLING_BACK, _S.FAILED) is _S.FAILED
    with pytest.raises(LifecycleTransitionError):
        validate_transition(_S.ROLLING_BACK, _S.READY)


def test_transition_table_is_deterministic():
    for current, target in _LEGAL_PAIRS:
        first = validate_transition(current, target)
        second = validate_transition(current, target)
        assert first is second is target
    assert LIFECYCLE_TRANSITIONS[_S.STARTING] == frozenset(
        {_S.READY, _S.DEGRADED, _S.ROLLING_BACK, _S.FAILED}
    )


def test_no_free_form_string_lifecycle_state_accepted():
    with pytest.raises(ValueError):
        RuntimeLifecycleState("NOT_A_REAL_STATE")

    with pytest.raises(LifecycleTransitionError):
        validate_transition("READY", "DEGRADED")

    with pytest.raises(LifecycleTransitionError):
        validate_transition(_S.READY, "DEGRADED")


def test_no_filesystem_or_environment_side_effects(monkeypatch, tmp_path):
    environ_before = dict(os.environ)

    def _forbidden_open(*_args, **_kwargs):
        raise AssertionError("lifecycle validation must not touch the filesystem")

    monkeypatch.setattr("builtins.open", _forbidden_open)

    for current, target in _LEGAL_PAIRS:
        validate_transition(current, target)
    for current, target in _ILLEGAL_PAIRS:
        with pytest.raises(LifecycleTransitionError):
            validate_transition(current, target)

    assert os.environ == environ_before
    assert list(tmp_path.iterdir()) == []
