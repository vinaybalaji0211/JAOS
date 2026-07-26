"""End-to-end tests for the JAOS Intelligence Context Manager."""

import json
from typing import Any

import pytest

from jaos.intelligence import (
    ContextBundle,
    ContextItem,
    ContextTrustLevel,
    IntelligenceComponentStateError,
    IntelligenceContextError,
    IntelligenceContextSource,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    ContextPolicy,
    DefaultIntelligenceContextManager,
    StaticContextSource,
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
    context_policy: str | None = None,
    permission_constraints: tuple[str, ...] = (),
) -> IntelligenceRequest:
    return IntelligenceRequest(
        objective="Assemble JAOS context",
        request_type=IntelligenceRequestType.CONTEXT,
        identity=create_identity(),
        context_policy=context_policy,
        permission_constraints=permission_constraints,
    )


def create_item(**overrides: Any) -> ContextItem:
    values: dict[str, Any] = {
        "item_id": "context-001",
        "context_type": IntelligenceContextType.USER,
        "content": "Approved JAOS context",
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


class FailingContextSource(IntelligenceContextSource):
    """Context source used to verify source failure isolation."""

    def __init__(self, source_name: str = "failing") -> None:
        self._source_name = source_name
        self._ready = False

    @property
    def component_name(self) -> str:
        return f"context-source:{self._source_name}"

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def is_ready(self) -> bool:
        return self._ready

    def initialize(self) -> None:
        self._ready = True

    def shutdown(self) -> None:
        self._ready = False

    def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        raise RuntimeError("simulated context source failure")


def test_context_manager_lifecycle() -> None:
    manager = DefaultIntelligenceContextManager()

    assert manager.component_name == "intelligence-context-manager"
    assert manager.is_ready is False

    manager.initialize()

    assert manager.is_ready is True

    manager.shutdown()

    assert manager.is_ready is False


def test_context_manager_requires_ready_state() -> None:
    manager = DefaultIntelligenceContextManager()

    with pytest.raises(IntelligenceComponentStateError):
        manager.assemble_context(create_request())


def test_context_manager_assembles_candidate_items() -> None:
    manager = DefaultIntelligenceContextManager()
    manager.initialize()
    item = create_item()
    request = create_request()

    bundle = manager.assemble_context(
        request,
        (item,),
    )

    assert isinstance(bundle, ContextBundle)
    assert bundle.items == (item,)
    assert bundle.request_id == request.request_id
    assert bundle.identity == create_identity()
    assert bundle.total_estimated_tokens == 10
    assert bundle.excluded_item_ids == ()
    assert bundle.truncated is False
    assert bundle.context_policy == "default"
    assert bundle.metadata["resolved_policy_name"] == "default"


def test_context_manager_assembles_registered_source() -> None:
    item = create_item(
        item_id="system-context",
        identity=IntelligenceIdentity(IntelligenceScope.GLOBAL),
        context_type=IntelligenceContextType.SYSTEM,
        trust_level=ContextTrustLevel.TRUSTED_SYSTEM,
        source="system",
    )
    source = StaticContextSource("system", (item,))
    source.initialize()

    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.initialize()

    bundle = manager.assemble_context(create_request())

    assert bundle.items == (item,)
    assert bundle.metadata["registered_source_count"] == 1
    assert bundle.metadata["source_errors"] == {}


def test_context_manager_skips_source_that_is_not_ready() -> None:
    source = StaticContextSource(
        "system",
        (create_item(item_id="system-context"),),
    )
    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.initialize()

    bundle = manager.assemble_context(create_request())

    assert bundle.items == ()
    assert bundle.metadata["source_errors"] == {
        "system": "context source is not ready"
    }


def test_context_manager_can_fail_on_unready_source() -> None:
    source = StaticContextSource(
        "system",
        (create_item(item_id="system-context"),),
    )
    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.register_policy(
        "strict-source",
        ContextPolicy(fail_on_source_error=True),
    )
    manager.initialize()

    with pytest.raises(IntelligenceContextError):
        manager.assemble_context(
            create_request(context_policy="strict-source")
        )


def test_context_manager_isolates_source_failure() -> None:
    source = FailingContextSource()
    source.initialize()

    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.initialize()

    bundle = manager.assemble_context(create_request())

    assert bundle.items == ()
    assert "failing" in bundle.metadata["source_errors"]
    assert (
        "simulated context source failure"
        in bundle.metadata["source_errors"]["failing"]
    )


def test_context_manager_can_fail_on_source_exception() -> None:
    source = FailingContextSource()
    source.initialize()

    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.register_policy(
        "strict-source",
        ContextPolicy(fail_on_source_error=True),
    )
    manager.initialize()

    with pytest.raises(IntelligenceContextError):
        manager.assemble_context(
            create_request(context_policy="strict-source")
        )


def test_context_manager_filters_by_permission() -> None:
    allowed = create_item(
        item_id="allowed",
        permission_constraints=("memory.read",),
    )
    denied = create_item(
        item_id="denied",
        content="Restricted context",
        permission_constraints=("memory.write",),
    )
    request = create_request(
        permission_constraints=("memory.read",)
    )

    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    bundle = manager.assemble_context(
        request,
        (allowed, denied),
    )

    assert bundle.items == (allowed,)
    assert bundle.excluded_item_ids == ("denied",)
    assert (
        bundle.metadata["filter"]["exclusion_reasons"]["denied"]
        == "permission_scope_mismatch"
    )


def test_context_manager_ranks_before_budget_selection() -> None:
    low = create_item(
        item_id="low",
        content="Low priority",
        relevance=0.1,
        importance=0.1,
        confidence=0.1,
    )
    high = create_item(
        item_id="high",
        content="High priority",
        relevance=1.0,
        importance=1.0,
        confidence=1.0,
    )

    manager = DefaultIntelligenceContextManager()
    manager.register_policy(
        "single-item",
        ContextPolicy(
            max_tokens=100,
            max_items=1,
        ),
    )
    manager.initialize()

    bundle = manager.assemble_context(
        create_request(context_policy="single-item"),
        (low, high),
    )

    assert bundle.items == (high,)
    assert bundle.excluded_item_ids == ("low",)
    assert bundle.truncated is True
    assert bundle.context_policy == "single-item"


def test_context_manager_deduplicates_after_ranking() -> None:
    lower = create_item(
        item_id="lower",
        source="secondary",
        relevance=0.3,
        importance=0.3,
        confidence=0.3,
    )
    higher = create_item(
        item_id="higher",
        source="trusted",
        relevance=1.0,
        importance=1.0,
        confidence=1.0,
    )

    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    bundle = manager.assemble_context(
        create_request(),
        (lower, higher),
    )

    assert bundle.items == (higher,)
    assert bundle.excluded_item_ids == ("lower",)
    assert bundle.metadata["deduplication"]["duplicate_of"] == {
        "lower": "higher"
    }


def test_context_manager_preserves_detected_conflicts() -> None:
    first = create_item(
        item_id="first",
        content="JAOS",
        metadata={"conflict_key": "system.name"},
    )
    second = create_item(
        item_id="second",
        content="JARVIS OS",
        metadata={"conflict_key": "system.name"},
    )

    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    bundle = manager.assemble_context(
        create_request(),
        (first, second),
    )

    assert set(bundle.conflict_item_ids) == {"first", "second"}
    assert bundle.metadata["conflicts"]["has_conflicts"] is True


def test_context_manager_can_fail_on_conflict() -> None:
    first = create_item(
        item_id="first",
        content="JAOS",
        metadata={"conflict_key": "system.name"},
    )
    second = create_item(
        item_id="second",
        content="JARVIS OS",
        metadata={"conflict_key": "system.name"},
    )

    manager = DefaultIntelligenceContextManager()
    manager.register_policy(
        "strict-conflict",
        ContextPolicy(fail_on_conflict=True),
    )
    manager.initialize()

    with pytest.raises(IntelligenceContextError):
        manager.assemble_context(
            create_request(context_policy="strict-conflict"),
            (first, second),
        )


def test_context_manager_rejects_unknown_policy_name() -> None:
    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    with pytest.raises(IntelligenceContextError):
        manager.assemble_context(
            create_request(context_policy="missing-policy")
        )


def test_context_manager_rejects_duplicate_candidate_ids() -> None:
    first = create_item(item_id="duplicate")
    second = create_item(
        item_id="duplicate",
        content="Different value",
    )

    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    with pytest.raises(IntelligenceContextError):
        manager.assemble_context(
            create_request(),
            (first, second),
        )


def test_context_manager_validates_bundle_identity() -> None:
    mismatched_item = create_item(
        identity=create_identity("another-user")
    )
    bundle = ContextBundle(
        request_id="request-001",
        identity=create_identity(),
        items=(mismatched_item,),
        max_tokens=100,
    )
    manager = DefaultIntelligenceContextManager()

    with pytest.raises(IntelligenceContextError):
        manager.validate_context(bundle)


def test_context_manager_validates_policy_budget_match() -> None:
    manager = DefaultIntelligenceContextManager()
    manager.register_policy(
        "compact",
        ContextPolicy(
            max_tokens=200,
            max_items=10,
        ),
    )
    bundle = ContextBundle(
        request_id="request-001",
        identity=create_identity(),
        items=(),
        max_tokens=100,
        context_policy="compact",
    )

    with pytest.raises(IntelligenceContextError):
        manager.validate_context(bundle)


def test_context_manager_register_and_unregister_source() -> None:
    source = StaticContextSource("system")
    manager = DefaultIntelligenceContextManager()

    manager.register_source(source)

    assert manager.source_registry.contains("system")

    removed = manager.unregister_source("system")

    assert removed is source
    assert len(manager.source_registry) == 0


def test_context_manager_register_and_unregister_policy() -> None:
    policy = ContextPolicy(max_tokens=100)
    manager = DefaultIntelligenceContextManager()

    manager.register_policy("compact", policy)

    assert manager.policy_registry.get_policy("compact") is policy

    removed = manager.unregister_policy("compact")

    assert removed is policy
    assert manager.policy_registry.contains("compact") is False


def test_context_bundle_metadata_is_json_serializable() -> None:
    manager = DefaultIntelligenceContextManager()
    manager.initialize()

    bundle = manager.assemble_context(
        create_request(),
        (create_item(),),
    )

    encoded = json.dumps(bundle.to_dict(), sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded["request_id"] == bundle.request_id
    assert decoded["context_policy"] == "default"
    assert decoded["metadata"]["selected_item_count"] == 1
    assert decoded["metadata"]["resolved_policy_name"] == "default"
    assert decoded["metadata"]["source_errors"] == {}