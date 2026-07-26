"""Tests for JAOS context filtering and ranking."""

import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from jaos.intelligence import (
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ContextFilter,
    ContextPolicy,
    ContextRanker,
)


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_request(
    *,
    permission_constraints: tuple[str, ...] = (),
) -> IntelligenceRequest:
    return IntelligenceRequest(
        objective="Assemble context",
        request_type=IntelligenceRequestType.CONTEXT,
        identity=create_identity(),
        permission_constraints=permission_constraints,
    )


def create_item(**overrides: Any) -> ContextItem:
    values: dict[str, Any] = {
        "item_id": "context-001",
        "context_type": IntelligenceContextType.USER,
        "content": "Approved user context",
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


def test_filter_includes_approved_item() -> None:
    item = create_item()
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(),
    )

    assert result.included_items == (item,)
    assert result.excluded_item_ids == ()
    assert result.exclusion_reasons == {}


def test_filter_allows_global_context() -> None:
    item = create_item(
        identity=IntelligenceIdentity(IntelligenceScope.GLOBAL)
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(),
    )

    assert result.included_items == (item,)


def test_filter_rejects_disallowed_context_type() -> None:
    item = create_item(
        context_type=IntelligenceContextType.MEMORY
    )
    policy = ContextPolicy(
        allowed_context_types=(IntelligenceContextType.USER,)
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        policy,
    )

    assert result.included_items == ()
    assert result.exclusion_reasons[item.item_id] == (
        "context_type_not_allowed"
    )


def test_filter_rejects_disallowed_trust_level() -> None:
    item = create_item(
        trust_level=ContextTrustLevel.EXTERNAL_UNTRUSTED
    )
    policy = ContextPolicy(
        allowed_trust_levels=(
            ContextTrustLevel.TRUSTED_SYSTEM,
            ContextTrustLevel.USER_PROVIDED,
        )
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        policy,
    )

    assert result.exclusion_reasons[item.item_id] == (
        "trust_level_not_allowed"
    )


def test_filter_rejects_low_relevance() -> None:
    item = create_item(relevance=0.4)
    policy = ContextPolicy(minimum_relevance=0.5)
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        policy,
    )

    assert result.exclusion_reasons[item.item_id] == (
        "below_minimum_relevance"
    )


def test_filter_rejects_low_importance() -> None:
    item = create_item(importance=0.4)
    policy = ContextPolicy(minimum_importance=0.5)
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        policy,
    )

    assert result.exclusion_reasons[item.item_id] == (
        "below_minimum_importance"
    )


def test_filter_rejects_expired_item() -> None:
    now = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)
    item = create_item(
        created_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(),
        now=now,
    )

    assert result.exclusion_reasons[item.item_id] == "expired"


def test_filter_can_include_expired_item_by_policy() -> None:
    now = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)
    item = create_item(
        created_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(include_expired=True),
        now=now,
    )

    assert result.included_items == (item,)


def test_filter_rejects_identity_scope_mismatch() -> None:
    item = create_item(identity=create_identity("another-user"))
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(),
    )

    assert result.exclusion_reasons[item.item_id] == (
        "identity_scope_mismatch"
    )


def test_filter_rejects_missing_permission() -> None:
    item = create_item(
        permission_constraints=("memory.read",)
    )
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(),
    )

    assert result.exclusion_reasons[item.item_id] == (
        "permission_scope_mismatch"
    )


def test_filter_accepts_matching_permission() -> None:
    item = create_item(
        permission_constraints=("memory.read",)
    )
    request = create_request(
        permission_constraints=("memory.read", "system.status")
    )
    result = ContextFilter().filter_items(
        request,
        (item,),
        ContextPolicy(),
    )

    assert result.included_items == (item,)


def test_filter_rejects_duplicate_item_ids() -> None:
    first = create_item(item_id="duplicate")
    second = create_item(
        item_id="duplicate",
        content="Different content",
    )

    with pytest.raises(IntelligenceContextError):
        ContextFilter().filter_items(
            create_request(),
            (first, second),
            ContextPolicy(),
        )


def test_filter_requires_aware_now() -> None:
    with pytest.raises(ValueError):
        ContextFilter().filter_items(
            create_request(),
            (create_item(),),
            ContextPolicy(),
            now=datetime.now(),
        )


def test_filter_result_is_json_serializable() -> None:
    item = create_item(relevance=0.1)
    result = ContextFilter().filter_items(
        create_request(),
        (item,),
        ContextPolicy(minimum_relevance=0.5),
    )

    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["excluded_item_ids"] == [item.item_id]
    assert decoded["exclusion_reasons"][item.item_id] == (
        "below_minimum_relevance"
    )


def test_ranker_orders_highest_score_first() -> None:
    low = create_item(
        item_id="low",
        relevance=0.2,
        importance=0.2,
        confidence=0.2,
    )
    high = create_item(
        item_id="high",
        relevance=0.9,
        importance=0.9,
        confidence=0.9,
    )

    result = ContextRanker().rank_items((low, high))

    assert result.ranked_items == (high, low)
    assert result.scores["high"] > result.scores["low"]


def test_ranker_uses_trust_as_part_of_score() -> None:
    external = create_item(
        item_id="external",
        trust_level=ContextTrustLevel.EXTERNAL_UNTRUSTED,
    )
    system = create_item(
        item_id="system",
        trust_level=ContextTrustLevel.TRUSTED_SYSTEM,
    )

    result = ContextRanker().rank_items((external, system))

    assert result.ranked_items[0] is system
    assert result.scores["system"] > result.scores["external"]


def test_ranker_normalizes_custom_weights() -> None:
    ranker = ContextRanker(
        relevance_weight=10.0,
        importance_weight=0.0,
        confidence_weight=0.0,
        trust_weight=0.0,
    )
    item = create_item(relevance=0.75)

    assert ranker.score_item(item) == pytest.approx(0.75)


def test_ranker_rejects_all_zero_weights() -> None:
    with pytest.raises(ValueError):
        ContextRanker(
            relevance_weight=0.0,
            importance_weight=0.0,
            confidence_weight=0.0,
            trust_weight=0.0,
        )


def test_ranker_rejects_negative_weight() -> None:
    with pytest.raises(ValueError):
        ContextRanker(relevance_weight=-1.0)


def test_ranker_rejects_invalid_item() -> None:
    with pytest.raises(TypeError):
        ContextRanker().score_item("invalid item")


def test_ranking_result_is_json_serializable() -> None:
    item = create_item()
    result = ContextRanker().rank_items((item,))
    decoded = json.loads(json.dumps(result.to_dict()))

    assert decoded["ranked_item_ids"] == [item.item_id]
    assert item.item_id in decoded["scores"]