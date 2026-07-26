"""Tests for protected context budget enforcement."""

from typing import Any

import pytest

from jaos.intelligence import (
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ContextBudgetManager,
    ContextPolicy,
)


def create_item(**overrides: Any) -> ContextItem:
    values: dict[str, Any] = {
        "item_id": "context-001",
        "context_type": IntelligenceContextType.USER,
        "content": "Context content",
        "identity": IntelligenceIdentity(
            IntelligenceScope.USER,
            "vinay",
        ),
        "source": "test",
        "trust_level": ContextTrustLevel.TRUSTED_INTERNAL,
        "relevance": 0.8,
        "importance": 0.8,
        "confidence": 0.9,
        "estimated_tokens": 10,
    }
    values.update(overrides)
    return ContextItem(**values)


def test_permission_context_cannot_be_truncated() -> None:
    optional_item = create_item(
        item_id="optional",
        relevance=1.0,
    )
    permission_item = create_item(
        item_id="permission",
        context_type=IntelligenceContextType.PERMISSION,
        content="File writes require explicit approval",
        relevance=0.1,
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=1,
    )

    result = ContextBudgetManager().select_items(
        (optional_item, permission_item),
        policy,
    )

    assert result.selected_items == (permission_item,)
    assert result.excluded_item_ids == ("optional",)
    assert result.truncated is True


def test_required_context_metadata_prevents_truncation() -> None:
    optional_item = create_item(item_id="optional")
    required_item = create_item(
        item_id="required",
        metadata={"required_context": True},
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=1,
    )

    result = ContextBudgetManager().select_items(
        (optional_item, required_item),
        policy,
    )

    assert result.selected_items == (required_item,)
    assert result.excluded_item_ids == ("optional",)


def test_security_constraint_metadata_prevents_truncation() -> None:
    optional_item = create_item(item_id="optional")
    security_item = create_item(
        item_id="security",
        metadata={"security_constraint": True},
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=1,
    )

    result = ContextBudgetManager().select_items(
        (optional_item, security_item),
        policy,
    )

    assert result.selected_items == (security_item,)
    assert result.excluded_item_ids == ("optional",)


def test_protected_context_over_token_budget_fails() -> None:
    security_item = create_item(
        item_id="security",
        context_type=IntelligenceContextType.PERMISSION,
        estimated_tokens=50,
    )
    policy = ContextPolicy(
        max_tokens=20,
        max_items=10,
    )

    with pytest.raises(IntelligenceContextError):
        ContextBudgetManager().select_items(
            (security_item,),
            policy,
        )


def test_protected_context_over_item_limit_fails() -> None:
    first = create_item(
        item_id="first",
        context_type=IntelligenceContextType.PERMISSION,
    )
    second = create_item(
        item_id="second",
        metadata={"required_context": True},
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=1,
    )

    with pytest.raises(IntelligenceContextError):
        ContextBudgetManager().select_items(
            (first, second),
            policy,
        )


@pytest.mark.parametrize(
    "metadata",
    [
        {"required_context": "yes"},
        {"security_constraint": 1},
    ],
)
def test_protected_context_flags_must_be_boolean(
    metadata: dict[str, Any],
) -> None:
    item = create_item(metadata=metadata)

    with pytest.raises(TypeError):
        ContextBudgetManager().select_items(
            (item,),
            ContextPolicy(),
        )


def test_protected_and_optional_context_fit_together() -> None:
    optional_item = create_item(
        item_id="optional",
        estimated_tokens=10,
    )
    security_item = create_item(
        item_id="security",
        context_type=IntelligenceContextType.PERMISSION,
        estimated_tokens=10,
    )
    policy = ContextPolicy(
        max_tokens=20,
        max_items=2,
    )

    result = ContextBudgetManager().select_items(
        (optional_item, security_item),
        policy,
    )

    assert result.selected_items == (
        optional_item,
        security_item,
    )
    assert result.total_estimated_tokens == 20
    assert result.truncated is False