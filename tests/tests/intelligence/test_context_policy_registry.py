"""Tests for context policy, source registry, and static sources."""

import json

import pytest

from jaos.intelligence import (
    ContextItem,
    ContextTrustLevel,
    IntelligenceComponentStateError,
    IntelligenceContextError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ContextPolicy,
    ContextSourceRegistry,
    StaticContextSource,
)


def create_identity() -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )


def create_request() -> IntelligenceRequest:
    return IntelligenceRequest(
        objective="Explain JAOS",
        request_type=IntelligenceRequestType.CONTEXT,
        identity=create_identity(),
    )


def create_item(
    *,
    item_id: str = "context-001",
) -> ContextItem:
    return ContextItem(
        item_id=item_id,
        context_type=IntelligenceContextType.SYSTEM,
        content="JAOS approved architecture",
        identity=IntelligenceIdentity(IntelligenceScope.GLOBAL),
        source="static",
        trust_level=ContextTrustLevel.TRUSTED_SYSTEM,
        relevance=0.9,
        importance=0.9,
        confidence=1.0,
    )


def create_source(
    *,
    source_name: str = "system",
) -> StaticContextSource:
    return StaticContextSource(
        source_name=source_name,
        items=(create_item(),),
    )


def test_context_policy_defaults() -> None:
    policy = ContextPolicy()

    assert policy.max_tokens == 4096
    assert policy.max_items == 64
    assert policy.minimum_relevance == 0.0
    assert policy.minimum_importance == 0.0
    assert policy.include_expired is False
    assert policy.fail_on_source_error is False
    assert policy.fail_on_conflict is False
    assert policy.deduplicate is True


def test_context_policy_from_empty_mapping_uses_defaults() -> None:
    assert ContextPolicy.from_mapping({}) == ContextPolicy()


def test_context_policy_normalizes_enum_strings() -> None:
    policy = ContextPolicy.from_mapping(
        {
            "max_tokens": 1000,
            "max_items": 10,
            "allowed_context_types": ["user", "memory"],
            "allowed_trust_levels": [
                "user_provided",
                "retrieved_memory",
            ],
        }
    )

    assert policy.allowed_context_types == (
        IntelligenceContextType.USER,
        IntelligenceContextType.MEMORY,
    )
    assert policy.allowed_trust_levels == (
        ContextTrustLevel.USER_PROVIDED,
        ContextTrustLevel.RETRIEVED_MEMORY,
    )


def test_context_policy_deduplicates_allowed_values() -> None:
    policy = ContextPolicy.from_mapping(
        {
            "allowed_context_types": ["user", "user"],
            "allowed_trust_levels": [
                "trusted_internal",
                "trusted_internal",
            ],
        }
    )

    assert policy.allowed_context_types == (
        IntelligenceContextType.USER,
    )
    assert policy.allowed_trust_levels == (
        ContextTrustLevel.TRUSTED_INTERNAL,
    )


def test_context_policy_rejects_unknown_fields() -> None:
    with pytest.raises(IntelligenceContextError):
        ContextPolicy.from_mapping({"unknown_policy": True})


@pytest.mark.parametrize("field_name", ["max_tokens", "max_items"])
@pytest.mark.parametrize("value", [0, -1])
def test_context_policy_requires_positive_limits(
    field_name: str,
    value: int,
) -> None:
    with pytest.raises(ValueError):
        ContextPolicy.from_mapping({field_name: value})


@pytest.mark.parametrize(
    "field_name",
    ["minimum_relevance", "minimum_importance"],
)
@pytest.mark.parametrize("value", [-0.01, 1.01])
def test_context_policy_validates_scores(
    field_name: str,
    value: float,
) -> None:
    with pytest.raises(ValueError):
        ContextPolicy.from_mapping({field_name: value})


def test_context_policy_is_json_serializable() -> None:
    encoded = json.dumps(ContextPolicy().to_dict())

    assert isinstance(encoded, str)
    assert '"max_tokens": 4096' in encoded


def test_static_context_source_lifecycle() -> None:
    source = create_source()

    assert source.component_name == "context-source:system"
    assert source.source_name == "system"
    assert source.is_ready is False

    source.initialize()

    assert source.is_ready is True

    collected_items = source.collect_context(create_request())

    assert len(collected_items) == 1
    assert collected_items[0].item_id == "context-001"
    assert collected_items[0].content == "JAOS approved architecture"
    assert (
        collected_items[0].trust_level
        is ContextTrustLevel.TRUSTED_SYSTEM
    )

    source.shutdown()

    assert source.is_ready is False


def test_static_context_source_requires_ready_state() -> None:
    source = create_source()

    with pytest.raises(IntelligenceComponentStateError):
        source.collect_context(create_request())


def test_static_context_source_rejects_duplicate_item_ids() -> None:
    item = create_item()

    with pytest.raises(ValueError):
        StaticContextSource("duplicate", (item, item))


def test_context_source_registry_registration() -> None:
    registry = ContextSourceRegistry()
    source = create_source()

    registry.register_source(source)

    assert len(registry) == 1
    assert registry.contains("SYSTEM")
    assert registry.get_source(" system ") is source
    assert registry.list_sources() == (source,)


def test_context_source_registry_rejects_duplicate_names() -> None:
    registry = ContextSourceRegistry()
    registry.register_source(create_source())

    with pytest.raises(IntelligenceContextError):
        registry.register_source(create_source())


def test_context_source_registry_unregisters_source() -> None:
    registry = ContextSourceRegistry()
    source = create_source()
    registry.register_source(source)

    removed = registry.unregister_source("SYSTEM")

    assert removed is source
    assert len(registry) == 0


@pytest.mark.parametrize(
    "operation",
    ["get", "unregister"],
)
def test_context_source_registry_rejects_missing_source(
    operation: str,
) -> None:
    registry = ContextSourceRegistry()

    with pytest.raises(IntelligenceContextError):
        if operation == "get":
            registry.get_source("missing")
        else:
            registry.unregister_source("missing")


def test_context_source_registry_clear() -> None:
    registry = ContextSourceRegistry()
    registry.register_source(create_source())

    registry.clear()

    assert len(registry) == 0
    assert registry.list_sources() == ()


def test_context_source_registry_requires_interface() -> None:
    registry = ContextSourceRegistry()

    with pytest.raises(TypeError):
        registry.register_source("invalid source")