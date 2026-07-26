"""Tests for shared AI Intelligence Platform enums."""

import json
from enum import Enum

import pytest

from jaos.intelligence import (
    AgentAvailabilityState,
    AgentTaskStatus,
    ContextTrustLevel,
    ConversationRole,
    ConversationSessionState,
    IntelligenceContextType,
    IntelligenceRequestType,
    IntelligenceResultStatus,
    ProposalStatus,
    RiskLevel,
)


ENUM_CASES = (
    (
        AgentAvailabilityState,
        {
            "available",
            "busy",
            "unavailable",
            "unhealthy",
            "disabled",
        },
    ),
    (
        AgentTaskStatus,
        {
            "pending",
            "routed",
            "running",
            "succeeded",
            "failed",
            "rejected",
            "cancelled",
        },
    ),
    (
        ContextTrustLevel,
        {
            "trusted_system",
            "trusted_internal",
            "user_provided",
            "retrieved_memory",
            "external_untrusted",
        },
    ),
    (
        ConversationRole,
        {"system", "user", "assistant", "memory", "tool_result"},
    ),
    (
        ConversationSessionState,
        {"active", "interrupted", "closed", "failed"},
    ),
    (
        IntelligenceContextType,
        {
            "system",
            "user",
            "conversation",
            "memory",
            "identity",
            "runtime",
            "capability",
            "tool_result",
            "permission",
            "project",
        },
    ),
    (
        IntelligenceRequestType,
        {
            "conversation",
            "context",
            "reasoning",
            "planning",
            "agent_task",
            "execution_proposal",
        },
    ),
    (
        IntelligenceResultStatus,
        {
            "pending",
            "succeeded",
            "failed",
            "rejected",
            "requires_clarification",
            "requires_approval",
        },
    ),
    (
        ProposalStatus,
        {
            "draft",
            "validated",
            "submitted",
            "approved",
            "rejected",
            "cancelled",
        },
    ),
    (
        RiskLevel,
        {"none", "low", "medium", "high", "critical"},
    ),
)


@pytest.mark.parametrize(("enum_type", "expected_values"), ENUM_CASES)
def test_enum_values_are_stable(
    enum_type: type[Enum],
    expected_values: set[str],
) -> None:
    assert {member.value for member in enum_type} == expected_values


@pytest.mark.parametrize(("enum_type", "expected_values"), ENUM_CASES)
def test_enum_members_are_strings(
    enum_type: type[Enum],
    expected_values: set[str],
) -> None:
    assert all(isinstance(member, str) for member in enum_type)
    assert all(str(member.value) in expected_values for member in enum_type)


@pytest.mark.parametrize(("enum_type", "expected_values"), ENUM_CASES)
def test_enum_values_round_trip(
    enum_type: type[Enum],
    expected_values: set[str],
) -> None:
    for value in expected_values:
        assert enum_type(value).value == value


@pytest.mark.parametrize(("enum_type", "expected_values"), ENUM_CASES)
def test_enum_values_are_json_serializable(
    enum_type: type[Enum],
    expected_values: set[str],
) -> None:
    encoded = json.dumps([member for member in enum_type])
    assert set(json.loads(encoded)) == expected_values


def test_public_package_exports_all_shared_enums() -> None:
    exported_types = {
        AgentAvailabilityState,
        AgentTaskStatus,
        ContextTrustLevel,
        ConversationRole,
        ConversationSessionState,
        IntelligenceContextType,
        IntelligenceRequestType,
        IntelligenceResultStatus,
        ProposalStatus,
        RiskLevel,
    }

    assert len(exported_types) == 10