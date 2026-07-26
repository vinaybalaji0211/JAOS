"""Tests for the JAOS named context policy registry."""

import pytest

from jaos.intelligence import IntelligenceContextError
from jaos.intelligence.context import (
    ContextPolicy,
    ContextPolicyRegistry,
)


def test_policy_registry_contains_default_policy() -> None:
    registry = ContextPolicyRegistry()

    assert len(registry) == 1
    assert registry.contains("default")
    assert registry.list_policy_names() == ("default",)
    assert registry.resolve(None) == ContextPolicy()


def test_policy_registry_accepts_custom_default() -> None:
    default_policy = ContextPolicy(max_tokens=1024)
    registry = ContextPolicyRegistry(default_policy)

    assert registry.resolve(None) is default_policy
    assert registry.get_policy("default") is default_policy


def test_policy_registry_registers_named_policy() -> None:
    registry = ContextPolicyRegistry()
    policy = ContextPolicy(max_tokens=512)

    registry.register_policy(" Compact ", policy)

    assert registry.contains("compact")
    assert registry.get_policy("COMPACT") is policy
    assert registry.resolve(" compact ") is policy


def test_policy_registry_rejects_duplicate_name() -> None:
    registry = ContextPolicyRegistry()
    registry.register_policy(
        "compact",
        ContextPolicy(max_tokens=512),
    )

    with pytest.raises(IntelligenceContextError):
        registry.register_policy(
            "compact",
            ContextPolicy(max_tokens=256),
        )


def test_policy_registry_can_replace_policy() -> None:
    registry = ContextPolicyRegistry()
    original = ContextPolicy(max_tokens=512)
    replacement = ContextPolicy(max_tokens=256)

    registry.register_policy("compact", original)
    registry.register_policy(
        "compact",
        replacement,
        replace=True,
    )

    assert registry.get_policy("compact") is replacement


def test_policy_registry_rejects_unknown_policy() -> None:
    registry = ContextPolicyRegistry()

    with pytest.raises(IntelligenceContextError):
        registry.get_policy("missing")


def test_policy_registry_rejects_unregistered_resolution() -> None:
    registry = ContextPolicyRegistry()

    with pytest.raises(IntelligenceContextError):
        registry.resolve("missing")


def test_policy_registry_unregisters_custom_policy() -> None:
    registry = ContextPolicyRegistry()
    policy = ContextPolicy(max_tokens=512)
    registry.register_policy("compact", policy)

    removed = registry.unregister_policy("compact")

    assert removed is policy
    assert registry.contains("compact") is False


def test_policy_registry_protects_default_policy() -> None:
    registry = ContextPolicyRegistry()

    with pytest.raises(IntelligenceContextError):
        registry.unregister_policy("default")


def test_policy_registry_requires_policy_instance() -> None:
    registry = ContextPolicyRegistry()

    with pytest.raises(TypeError):
        registry.register_policy("invalid", "not a policy")


def test_policy_registry_requires_boolean_replace() -> None:
    registry = ContextPolicyRegistry()

    with pytest.raises(TypeError):
        registry.register_policy(
            "compact",
            ContextPolicy(),
            replace="yes",
        )