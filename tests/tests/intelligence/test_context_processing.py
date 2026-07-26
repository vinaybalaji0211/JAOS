"""Tests for JAOS context processing components."""

import json
from typing import Any

import pytest

from jaos.intelligence import (
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ContextBudgetManager,
    ContextConflictDetector,
    ContextDeduplicator,
    ContextPolicy,
    ContextTokenEstimator,
)


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_item(**overrides: Any) -> ContextItem:
    values: dict[str, Any] = {
        "item_id": "context-001",
        "context_type": IntelligenceContextType.USER,
        "content": "Approved context",
        "identity": create_identity(),
        "source": "test",
        "trust_level": ContextTrustLevel.USER_PROVIDED,
        "relevance": 0.8,
        "importance": 0.7,
        "confidence": 0.9,
        "estimated_tokens": 10,
    }
    values.update(overrides)
    return ContextItem(**values)


def test_deduplicator_retains_first_ranked_item() -> None:
    first = create_item(
        item_id="high-ranked",
        source="trusted-source",
    )
    duplicate = create_item(
        item_id="low-ranked",
        source="secondary-source",
    )

    result = ContextDeduplicator().deduplicate(
        (first, duplicate)
    )

    assert result.retained_items == (first,)
    assert result.duplicate_item_ids == ("low-ranked",)
    assert result.duplicate_of == {
        "low-ranked": "high-ranked"
    }


def test_deduplicator_preserves_different_content() -> None:
    first = create_item(item_id="first", content="Value A")
    second = create_item(item_id="second", content="Value B")

    result = ContextDeduplicator().deduplicate(
        (first, second)
    )

    assert result.retained_items == (first, second)
    assert result.duplicate_item_ids == ()


def test_deduplicator_preserves_different_context_types() -> None:
    user_item = create_item(
        item_id="user",
        context_type=IntelligenceContextType.USER,
    )
    memory_item = create_item(
        item_id="memory",
        context_type=IntelligenceContextType.MEMORY,
    )

    result = ContextDeduplicator().deduplicate(
        (user_item, memory_item)
    )

    assert result.retained_items == (user_item, memory_item)


def test_deduplicator_preserves_different_identities() -> None:
    first = create_item(
        item_id="first",
        identity=create_identity("vinay"),
    )
    second = create_item(
        item_id="second",
        identity=create_identity("another-user"),
    )

    result = ContextDeduplicator().deduplicate(
        (first, second)
    )

    assert result.retained_items == (first, second)


def test_deduplication_result_is_json_serializable() -> None:
    first = create_item(item_id="first")
    duplicate = create_item(item_id="duplicate")
    result = ContextDeduplicator().deduplicate(
        (first, duplicate)
    )

    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["retained_item_ids"] == ["first"]
    assert decoded["duplicate_item_ids"] == ["duplicate"]
    assert decoded["duplicate_of"]["duplicate"] == "first"


def test_deduplicator_rejects_invalid_items() -> None:
    with pytest.raises(TypeError):
        ContextDeduplicator().deduplicate(("invalid",))


def test_conflict_detector_finds_different_values() -> None:
    first = create_item(
        item_id="name-a",
        content="JAOS",
        metadata={"conflict_key": "system.name"},
    )
    second = create_item(
        item_id="name-b",
        content="JARVIS OS",
        metadata={"conflict_key": "SYSTEM.NAME"},
    )

    result = ContextConflictDetector().detect_conflicts(
        (first, second)
    )

    assert result.has_conflicts is True
    assert result.conflict_item_ids == ("name-a", "name-b")
    assert result.conflict_groups == {
        "system.name": ("name-a", "name-b")
    }


def test_conflict_detector_ignores_equal_values() -> None:
    first = create_item(
        item_id="first",
        content="JAOS",
        metadata={"conflict_key": "system.name"},
    )
    second = create_item(
        item_id="second",
        content="JAOS",
        metadata={"conflict_key": "system.name"},
    )

    result = ContextConflictDetector().detect_conflicts(
        (first, second)
    )

    assert result.has_conflicts is False
    assert result.conflict_item_ids == ()


def test_conflict_detector_ignores_items_without_key() -> None:
    result = ContextConflictDetector().detect_conflicts(
        (
            create_item(item_id="first", content="A"),
            create_item(item_id="second", content="B"),
        )
    )

    assert result.has_conflicts is False


def test_conflict_detector_rejects_invalid_key() -> None:
    item = create_item(
        metadata={"conflict_key": 123}
    )

    with pytest.raises(TypeError):
        ContextConflictDetector().detect_conflicts((item,))


def test_conflict_result_is_json_serializable() -> None:
    first = create_item(
        item_id="first",
        content="A",
        metadata={"conflict_key": "value"},
    )
    second = create_item(
        item_id="second",
        content="B",
        metadata={"conflict_key": "value"},
    )
    result = ContextConflictDetector().detect_conflicts(
        (first, second)
    )

    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["has_conflicts"] is True
    assert decoded["conflict_groups"]["value"] == [
        "first",
        "second",
    ]


def test_token_estimator_preserves_existing_estimate() -> None:
    item = create_item(estimated_tokens=25)
    estimator = ContextTokenEstimator()

    assert estimator.estimate_item(item) == 25
    assert estimator.apply_estimate(item) is item


def test_token_estimator_calculates_missing_estimate() -> None:
    item = create_item(
        content="abcd",
        estimated_tokens=0,
    )
    estimator = ContextTokenEstimator(
        characters_per_token=4,
        item_overhead_tokens=2,
    )

    assert estimator.estimate_item(item) == 3


def test_token_estimator_applies_estimate_without_changing_id() -> None:
    item = create_item(estimated_tokens=0)
    estimated_item = ContextTokenEstimator().apply_estimate(item)

    assert estimated_item is not item
    assert estimated_item.item_id == item.item_id
    assert estimated_item.estimated_tokens > 0


@pytest.mark.parametrize(
    "field_name",
    ["characters_per_token", "item_overhead_tokens"],
)
def test_token_estimator_requires_positive_configuration(
    field_name: str,
) -> None:
    with pytest.raises(ValueError):
        ContextTokenEstimator(**{field_name: 0})


def test_token_estimator_rejects_invalid_item() -> None:
    with pytest.raises(TypeError):
        ContextTokenEstimator().estimate_item("invalid")


def test_budget_manager_selects_items_within_limits() -> None:
    first = create_item(
        item_id="first",
        estimated_tokens=10,
    )
    second = create_item(
        item_id="second",
        estimated_tokens=15,
    )
    policy = ContextPolicy(
        max_tokens=30,
        max_items=3,
    )

    result = ContextBudgetManager().select_items(
        (first, second),
        policy,
    )

    assert result.selected_items == (first, second)
    assert result.total_estimated_tokens == 25
    assert result.excluded_item_ids == ()
    assert result.truncated is False


def test_budget_manager_enforces_item_limit() -> None:
    first = create_item(
        item_id="first",
        estimated_tokens=5,
    )
    second = create_item(
        item_id="second",
        estimated_tokens=5,
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=1,
    )

    result = ContextBudgetManager().select_items(
        (first, second),
        policy,
    )

    assert result.selected_items == (first,)
    assert result.excluded_item_ids == ("second",)
    assert result.truncated is True


def test_budget_manager_enforces_token_limit() -> None:
    first = create_item(
        item_id="first",
        estimated_tokens=15,
    )
    second = create_item(
        item_id="second",
        estimated_tokens=15,
    )
    policy = ContextPolicy(
        max_tokens=20,
        max_items=10,
    )

    result = ContextBudgetManager().select_items(
        (first, second),
        policy,
    )

    assert result.selected_items == (first,)
    assert result.excluded_item_ids == ("second",)
    assert result.total_estimated_tokens == 15


def test_budget_manager_can_select_smaller_later_item() -> None:
    oversized = create_item(
        item_id="oversized",
        estimated_tokens=50,
    )
    smaller = create_item(
        item_id="smaller",
        estimated_tokens=10,
    )
    policy = ContextPolicy(
        max_tokens=20,
        max_items=10,
    )

    result = ContextBudgetManager().select_items(
        (oversized, smaller),
        policy,
    )

    assert result.selected_items == (smaller,)
    assert result.excluded_item_ids == ("oversized",)
    assert result.total_estimated_tokens == 10


def test_budget_manager_estimates_missing_tokens() -> None:
    item = create_item(
        content="Context without a source token estimate",
        estimated_tokens=0,
    )
    policy = ContextPolicy(
        max_tokens=100,
        max_items=10,
    )

    result = ContextBudgetManager().select_items(
        (item,),
        policy,
    )

    assert len(result.selected_items) == 1
    assert result.selected_items[0].estimated_tokens > 0
    assert result.total_estimated_tokens > 0


def test_budget_result_is_json_serializable() -> None:
    item = create_item(estimated_tokens=10)
    result = ContextBudgetManager().select_items(
        (item,),
        ContextPolicy(max_tokens=20),
    )

    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["selected_item_ids"] == [item.item_id]
    assert decoded["total_estimated_tokens"] == 10
    assert decoded["truncated"] is False