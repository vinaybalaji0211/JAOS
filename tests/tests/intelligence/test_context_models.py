"""Tests for AI Intelligence Platform context models."""

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from jaos.intelligence import (
    ContextBundle,
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceScope,
)


@pytest.fixture
def user_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


@pytest.fixture
def created_at() -> datetime:
    return datetime(2026, 1, 1, 10, tzinfo=timezone.utc)


def build_context_item(
    identity: IntelligenceIdentity,
    **overrides: object,
) -> ContextItem:
    arguments: dict[str, object] = {
        "context_type": IntelligenceContextType.MEMORY,
        "content": "JAOS Phase 8 is active",
        "identity": identity,
        "source": "memory",
        "trust_level": ContextTrustLevel.RETRIEVED_MEMORY,
        "item_id": "context-001",
        "estimated_tokens": 10,
    }
    arguments.update(overrides)

    return ContextItem(**arguments)  # type: ignore[arg-type]


def test_context_item_normalizes_valid_input(
    user_identity: IntelligenceIdentity,
    created_at: datetime,
) -> None:
    metadata = {"memory_id": "memory-001"}

    item = ContextItem(
        context_type=IntelligenceContextType.MEMORY,
        content=" JAOS Phase 8 is active ",
        identity=user_identity,
        source=" MEMORY ",
        trust_level=ContextTrustLevel.RETRIEVED_MEMORY,
        item_id=" context-001 ",
        relevance=1,
        importance=0.8,
        confidence=0.9,
        estimated_tokens=20,
        permission_constraints=(" Read ", "read", " Project "),
        metadata=metadata,
        created_at=created_at,
        expires_at=created_at + timedelta(hours=1),
    )

    metadata["memory_id"] = "changed"

    assert item.item_id == "context-001"
    assert item.content == "JAOS Phase 8 is active"
    assert item.source == "memory"
    assert item.relevance == 1.0
    assert item.importance == 0.8
    assert item.confidence == 0.9
    assert item.permission_constraints == ("read", "project")
    assert item.metadata == {"memory_id": "memory-001"}


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("item_id", ""),
        ("content", "   "),
        ("source", None),
    ],
)
def test_context_item_rejects_invalid_required_string(
    field_name: str,
    value: object,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be a non-empty string",
    ):
        build_context_item(
            user_identity,
            **{field_name: value},
        )


def test_context_item_rejects_invalid_context_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="context_type must be an instance",
    ):
        build_context_item(
            user_identity,
            context_type="memory",
        )


def test_context_item_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an instance",
    ):
        ContextItem(
            context_type=IntelligenceContextType.MEMORY,
            content="JAOS Phase 8",
            identity="vinay",  # type: ignore[arg-type]
            source="memory",
            trust_level=ContextTrustLevel.RETRIEVED_MEMORY,
        )


def test_context_item_rejects_invalid_trust_level(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="trust_level must be an instance",
    ):
        build_context_item(
            user_identity,
            trust_level="retrieved_memory",
        )


@pytest.mark.parametrize(
    "field_name",
    ["relevance", "importance", "confidence"],
)
def test_context_item_rejects_invalid_score_type(
    field_name: str,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field_name} must be a number",
    ):
        build_context_item(
            user_identity,
            **{field_name: True},
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("relevance", -0.1),
        ("relevance", 1.1),
        ("importance", -0.1),
        ("importance", 1.1),
        ("confidence", -0.1),
        ("confidence", 1.1),
    ],
)
def test_context_item_rejects_score_outside_unit_interval(
    field_name: str,
    value: float,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field_name} must be between",
    ):
        build_context_item(
            user_identity,
            **{field_name: value},
        )


def test_context_item_rejects_invalid_token_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="estimated_tokens must be an integer",
    ):
        build_context_item(
            user_identity,
            estimated_tokens=True,
        )


def test_context_item_rejects_negative_tokens(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="estimated_tokens cannot be negative",
    ):
        build_context_item(
            user_identity,
            estimated_tokens=-1,
        )


def test_context_item_rejects_string_permission_collection(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="permission_constraints must be a collection",
    ):
        build_context_item(
            user_identity,
            permission_constraints="read",
        )


def test_context_item_rejects_empty_permission(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="permission_constraints must contain",
    ):
        build_context_item(
            user_identity,
            permission_constraints=("read", "   "),
        )


def test_context_item_rejects_invalid_metadata(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="metadata must be a dictionary",
    ):
        build_context_item(
            user_identity,
            metadata=[],
        )


def test_context_item_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        build_context_item(
            user_identity,
            created_at=datetime(2026, 1, 1),
        )


def test_context_item_rejects_invalid_expiration_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="expires_at must be a datetime instance or None",
    ):
        build_context_item(
            user_identity,
            expires_at="tomorrow",
        )


def test_context_item_rejects_naive_expiration(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="expires_at must be timezone-aware",
    ):
        build_context_item(
            user_identity,
            expires_at=datetime(2027, 1, 1),
        )


def test_context_item_rejects_expiration_before_creation(
    user_identity: IntelligenceIdentity,
    created_at: datetime,
) -> None:
    with pytest.raises(
        ValueError,
        match="expires_at must be later than created_at",
    ):
        build_context_item(
            user_identity,
            created_at=created_at,
            expires_at=created_at,
        )


def test_context_item_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
    created_at: datetime,
) -> None:
    item = build_context_item(
        user_identity,
        created_at=created_at,
        relevance=0.9,
        permission_constraints=("read",),
    )

    decoded = json.loads(json.dumps(item.to_dict()))

    assert decoded["item_id"] == "context-001"
    assert decoded["context_type"] == "memory"
    assert decoded["identity"] == {
        "scope": "user",
        "identity_id": "vinay",
    }
    assert decoded["trust_level"] == "retrieved_memory"
    assert decoded["permission_constraints"] == ["read"]


def test_context_item_is_immutable(
    user_identity: IntelligenceIdentity,
) -> None:
    item = build_context_item(user_identity)

    with pytest.raises(FrozenInstanceError):
        item.content = "Changed"  # type: ignore[misc]


def test_context_bundle_accepts_minimum_valid_input(
    user_identity: IntelligenceIdentity,
) -> None:
    bundle = ContextBundle(
        request_id="request-001",
        identity=user_identity,
        bundle_id="bundle-001",
    )

    assert bundle.request_id == "request-001"
    assert bundle.bundle_id == "bundle-001"
    assert bundle.items == ()
    assert bundle.total_estimated_tokens == 0
    assert bundle.truncated is False


def test_context_bundle_normalizes_valid_input(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_context_item(
        user_identity,
        item_id="context-001",
        estimated_tokens=10,
    )
    second = build_context_item(
        user_identity,
        item_id="context-002",
        estimated_tokens=20,
    )
    metadata = {"source": "context-manager"}

    bundle = ContextBundle(
        request_id=" request-001 ",
        identity=user_identity,
        items=[first, second],  # type: ignore[arg-type]
        bundle_id=" bundle-001 ",
        max_tokens=50,
        context_policy=" DEFAULT ",
        excluded_item_ids=(" excluded-001 ", "excluded-001"),
        conflict_item_ids=(" context-002 ",),
        truncated=True,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert bundle.request_id == "request-001"
    assert bundle.bundle_id == "bundle-001"
    assert bundle.items == (first, second)
    assert bundle.total_estimated_tokens == 30
    assert bundle.context_policy == "default"
    assert bundle.excluded_item_ids == ("excluded-001",)
    assert bundle.conflict_item_ids == ("context-002",)
    assert bundle.metadata == {"source": "context-manager"}


def test_context_bundle_rejects_duplicate_item_ids(
    user_identity: IntelligenceIdentity,
) -> None:
    first = build_context_item(
        user_identity,
        item_id="context-001",
    )
    second = build_context_item(
        user_identity,
        item_id="context-001",
    )

    with pytest.raises(
        ValueError,
        match="context item IDs must be unique",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            items=(first, second),
        )


def test_context_bundle_rejects_invalid_item_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="items must contain only ContextItem instances",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            items=("invalid",),  # type: ignore[arg-type]
        )


def test_context_bundle_rejects_invalid_identity() -> None:
    with pytest.raises(
        TypeError,
        match="identity must be an instance",
    ):
        ContextBundle(
            request_id="request-001",
            identity="vinay",  # type: ignore[arg-type]
        )


def test_context_bundle_rejects_invalid_token_limit_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="max_tokens must be an integer or None",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            max_tokens=True,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("max_tokens", [0, -1])
def test_context_bundle_rejects_non_positive_token_limit(
    max_tokens: int,
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="max_tokens must be greater than zero",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            max_tokens=max_tokens,
        )


def test_context_bundle_rejects_items_over_token_limit(
    user_identity: IntelligenceIdentity,
) -> None:
    item = build_context_item(
        user_identity,
        estimated_tokens=20,
    )

    with pytest.raises(
        ValueError,
        match="context items exceed max_tokens",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            items=(item,),
            max_tokens=10,
        )


def test_context_bundle_rejects_included_excluded_item(
    user_identity: IntelligenceIdentity,
) -> None:
    item = build_context_item(user_identity)

    with pytest.raises(
        ValueError,
        match="excluded_item_ids must not reference included items",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            items=(item,),
            excluded_item_ids=("context-001",),
        )


def test_context_bundle_rejects_unknown_conflict_item(
    user_identity: IntelligenceIdentity,
) -> None:
    item = build_context_item(user_identity)

    with pytest.raises(
        ValueError,
        match="conflict_item_ids must reference included items",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            items=(item,),
            conflict_item_ids=("unknown",),
        )


def test_context_bundle_rejects_invalid_truncated_type(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        TypeError,
        match="truncated must be a boolean",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            truncated=1,  # type: ignore[arg-type]
        )


def test_context_bundle_rejects_naive_created_at(
    user_identity: IntelligenceIdentity,
) -> None:
    with pytest.raises(
        ValueError,
        match="created_at must be timezone-aware",
    ):
        ContextBundle(
            request_id="request-001",
            identity=user_identity,
            created_at=datetime(2026, 1, 1),
        )


def test_context_bundle_to_dict_is_json_serializable(
    user_identity: IntelligenceIdentity,
) -> None:
    item = build_context_item(user_identity)

    bundle = ContextBundle(
        request_id="request-001",
        identity=user_identity,
        items=(item,),
        bundle_id="bundle-001",
        max_tokens=100,
    )

    decoded = json.loads(json.dumps(bundle.to_dict()))

    assert decoded["bundle_id"] == "bundle-001"
    assert decoded["request_id"] == "request-001"
    assert decoded["total_estimated_tokens"] == 10
    assert decoded["items"][0]["item_id"] == "context-001"


def test_context_bundle_is_immutable(
    user_identity: IntelligenceIdentity,
) -> None:
    bundle = ContextBundle(
        request_id="request-001",
        identity=user_identity,
    )

    with pytest.raises(FrozenInstanceError):
        bundle.truncated = True  # type: ignore[misc]