"""Tests for AI Intelligence Platform identity models."""

import json
from dataclasses import FrozenInstanceError

import pytest

from jaos.intelligence import IntelligenceIdentity, IntelligenceScope


def test_intelligence_scope_values_are_stable() -> None:
    assert {scope.value for scope in IntelligenceScope} == {
        "global",
        "system",
        "user",
        "device",
        "session",
        "mission",
        "project",
        "agent",
    }


def test_global_identity_accepts_missing_identity_id() -> None:
    identity = IntelligenceIdentity(IntelligenceScope.GLOBAL)

    assert identity.scope is IntelligenceScope.GLOBAL
    assert identity.identity_id is None


@pytest.mark.parametrize(
    "scope",
    tuple(
        scope
        for scope in IntelligenceScope
        if scope is not IntelligenceScope.GLOBAL
    ),
)
def test_non_global_identity_normalizes_identity_id(
    scope: IntelligenceScope,
) -> None:
    identity = IntelligenceIdentity(scope, " vinay ")

    assert identity.scope is scope
    assert identity.identity_id == "vinay"


def test_global_identity_rejects_identity_id() -> None:
    with pytest.raises(
        ValueError,
        match="global intelligence identity must not define identity_id",
    ):
        IntelligenceIdentity(IntelligenceScope.GLOBAL, "global-id")


@pytest.mark.parametrize("identity_id", [None, "", "   "])
def test_non_global_identity_rejects_missing_identity_id(
    identity_id: str | None,
) -> None:
    with pytest.raises(
        ValueError,
        match="identity_id must be a non-empty string",
    ):
        IntelligenceIdentity(IntelligenceScope.USER, identity_id)


def test_identity_rejects_invalid_scope_type() -> None:
    with pytest.raises(
        TypeError,
        match="scope must be an instance of IntelligenceScope",
    ):
        IntelligenceIdentity("user", "vinay")  # type: ignore[arg-type]


def test_identity_to_dict_is_platform_independent() -> None:
    identity = IntelligenceIdentity(
        IntelligenceScope.PROJECT,
        "jaos",
    )

    assert identity.to_dict() == {
        "scope": "project",
        "identity_id": "jaos",
    }


def test_identity_dictionary_is_json_serializable() -> None:
    identity = IntelligenceIdentity(
        IntelligenceScope.SESSION,
        "session-001",
    )

    encoded = json.dumps(identity.to_dict())

    assert json.loads(encoded) == {
        "scope": "session",
        "identity_id": "session-001",
    }


def test_identity_is_immutable() -> None:
    identity = IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )

    with pytest.raises(FrozenInstanceError):
        identity.identity_id = "other"  # type: ignore[misc]