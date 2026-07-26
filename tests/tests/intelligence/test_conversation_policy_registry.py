"""Tests for conversation policies and their registry."""

import pytest

from jaos.intelligence import IntelligenceConversationError
from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_policy_registry import (
    ConversationPolicyRegistry,
)


def create_policy(
    *,
    policy_name: str = "default",
    max_history_turns: int = 100,
    reference_window_turns: int = 20,
    memory_candidates: bool = False,
    metadata: dict[str, object] | None = None,
) -> ConversationPolicy:
    return ConversationPolicy(
        policy_name=policy_name,
        context_policy="default",
        max_history_turns=max_history_turns,
        reference_window_turns=reference_window_turns,
        memory_candidate_submission_enabled=memory_candidates,
        metadata=dict(metadata or {}),
    )


def test_policy_defaults_are_safe() -> None:
    policy = ConversationPolicy()

    assert policy.policy_name == "default"
    assert policy.context_policy == "default"
    assert policy.allow_reference_resolution is True
    assert policy.allow_interruption is True
    assert policy.allow_continuation is True
    assert policy.require_context_bundle is True
    assert policy.working_memory_enabled is True
    assert policy.memory_candidate_submission_enabled is False


def test_policy_normalizes_and_serializes_values() -> None:
    policy = ConversationPolicy(
        policy_name=" Focused ",
        context_policy=" Strict ",
        max_history_turns=50,
        reference_window_turns=10,
        memory_candidate_submission_enabled=True,
    )

    serialized = policy.to_dict()

    assert policy.policy_name == "focused"
    assert policy.context_policy == "strict"
    assert serialized["policy_name"] == "focused"
    assert serialized["context_policy"] == "strict"
    assert (
        serialized["memory_candidate_submission_enabled"]
        is True
    )


def test_policy_copies_metadata() -> None:
    metadata = {"owner": "jaos"}
    policy = ConversationPolicy(metadata=metadata)

    metadata["owner"] = "changed"

    assert policy.metadata == {"owner": "jaos"}


def test_policy_rejects_zero_history_limit() -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        ConversationPolicy(max_history_turns=0)


def test_policy_rejects_boolean_history_limit() -> None:
    with pytest.raises(
        TypeError,
        match="must be an integer",
    ):
        ConversationPolicy(max_history_turns=True)


def test_policy_rejects_reference_window_above_history() -> None:
    with pytest.raises(
        ValueError,
        match="must not exceed",
    ):
        ConversationPolicy(
            max_history_turns=10,
            reference_window_turns=11,
        )


def test_policy_rejects_invalid_boolean_field() -> None:
    with pytest.raises(
        TypeError,
        match="must be a boolean",
    ):
        ConversationPolicy(
            allow_interruption="yes",
        )


def test_empty_registry_has_no_default_policy() -> None:
    registry = ConversationPolicyRegistry()

    assert len(registry) == 0
    assert registry.default_policy_name is None
    assert registry.list_policies() == ()

    with pytest.raises(
        IntelligenceConversationError,
        match="default conversation policy",
    ):
        registry.resolve_policy()


def test_first_registered_policy_becomes_default() -> None:
    registry = ConversationPolicyRegistry()
    policy = create_policy()

    registry.register_policy(policy)

    assert registry.default_policy_name == "default"
    assert registry.resolve_policy() == policy


def test_registry_can_register_explicit_default() -> None:
    registry = ConversationPolicyRegistry()
    first = create_policy(policy_name="first")
    second = create_policy(policy_name="second")

    registry.register_policy(first)
    registry.register_policy(second, make_default=True)

    assert registry.default_policy_name == "second"
    assert registry.resolve_policy() == second


def test_registry_rejects_duplicate_policy() -> None:
    registry = ConversationPolicyRegistry()
    registry.register_policy(create_policy())

    with pytest.raises(
        IntelligenceConversationError,
        match="already registered",
    ):
        registry.register_policy(create_policy())


def test_registry_can_replace_policy() -> None:
    registry = ConversationPolicyRegistry()
    original = create_policy()
    replacement = create_policy(
        max_history_turns=10,
        reference_window_turns=5,
    )

    registry.register_policy(original)
    registry.register_policy(replacement, replace=True)

    assert registry.get_policy("default") == replacement


def test_registry_isolates_policy_metadata() -> None:
    registry = ConversationPolicyRegistry()
    policy = create_policy(metadata={"owner": "jaos"})

    registry.register_policy(policy)

    policy.metadata["owner"] = "changed-original"

    loaded = registry.get_policy("default")
    loaded.metadata["owner"] = "changed-return-value"

    assert registry.get_policy("default").metadata == {
        "owner": "jaos"
    }


def test_registry_can_change_default_policy() -> None:
    registry = ConversationPolicyRegistry()
    first = create_policy(policy_name="first")
    second = create_policy(policy_name="second")

    registry.register_policy(first)
    registry.register_policy(second)
    registry.set_default_policy("second")

    assert registry.default_policy_name == "second"
    assert registry.resolve_policy() == second


def test_unregistering_default_selects_deterministic_fallback() -> None:
    registry = ConversationPolicyRegistry()
    beta = create_policy(policy_name="beta")
    alpha = create_policy(policy_name="alpha")
    current = create_policy(policy_name="current")

    registry.register_policy(current)
    registry.register_policy(beta)
    registry.register_policy(alpha)

    removed = registry.unregister_policy("current")

    assert removed == current
    assert registry.default_policy_name == "alpha"
    assert registry.resolve_policy() == alpha


def test_registry_lists_policies_by_name() -> None:
    registry = ConversationPolicyRegistry()
    beta = create_policy(policy_name="beta")
    alpha = create_policy(policy_name="alpha")

    registry.register_policy(beta)
    registry.register_policy(alpha)

    assert registry.list_policies() == (alpha, beta)


def test_registry_contains_and_length_track_policies() -> None:
    registry = ConversationPolicyRegistry()

    assert registry.contains("default") is False

    registry.register_policy(create_policy())

    assert registry.contains(" DEFAULT ") is True
    assert len(registry) == 1

    registry.unregister_policy("default")

    assert registry.contains("default") is False
    assert len(registry) == 0


def test_registry_rejects_missing_policy() -> None:
    registry = ConversationPolicyRegistry()

    with pytest.raises(
        IntelligenceConversationError,
        match="policy not found",
    ):
        registry.get_policy("missing")


def test_registry_rejects_invalid_policy_type() -> None:
    registry = ConversationPolicyRegistry()

    with pytest.raises(
        TypeError,
        match="must be a ConversationPolicy",
    ):
        registry.register_policy("invalid")


def test_registry_rejects_empty_policy_name() -> None:
    registry = ConversationPolicyRegistry()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        registry.contains(" ")