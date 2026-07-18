from __future__ import annotations

from dataclasses import replace

import pytest

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.providers.in_memory_store import InMemoryStore
from jaos.memory.providers.in_memory_transaction import (
    InMemoryTransaction,
)


@pytest.fixture
def memory_type() -> MemoryType:
    """
    Return a valid memory type.
    """
    return next(iter(MemoryType))


@pytest.fixture
def global_identity() -> MemoryIdentity:
    """
    Return a valid global memory identity.
    """
    return MemoryIdentity(scope=MemoryScope.GLOBAL)


def build_record(
    *,
    memory_id: str,
    content: str,
    memory_type: MemoryType,
    identity: MemoryIdentity,
    importance: float = 0.5,
    confidence: float = 1.0,
) -> MemoryRecord:
    """
    Build a valid memory record for transaction tests.
    """
    return MemoryRecord(
        memory_id=memory_id,
        content=content,
        memory_type=memory_type,
        identity=identity,
        source="transaction-unit-test",
        importance=importance,
        confidence=confidence,
        metadata=MemoryMetadata(
            values={
                "tags": ("transaction",),
            }
        ),
    )


def test_transaction_commit_persists_created_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        memory_id="commit-create",
        content="Committed memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.create(record)
    transaction.commit()

    assert store.get("commit-create") == record
    assert store.count() == 1


def test_transaction_rollback_discards_created_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        memory_id="rollback-create",
        content="Rolled-back memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.create(record)
    transaction.rollback()

    assert store.get("rollback-create") is None
    assert store.count() == 0


def test_context_manager_commits_on_success(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        memory_id="context-commit",
        content="Context committed memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    with InMemoryTransaction(store) as transaction:
        transaction.create(record)

    assert store.get("context-commit") == record
    assert store.count() == 1


def test_context_manager_rolls_back_on_exception(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    existing = build_record(
        memory_id="existing-record",
        content="Existing memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    pending = build_record(
        memory_id="pending-record",
        content="Pending memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    store.create(existing)

    with pytest.raises(RuntimeError, match="forced failure"):
        with InMemoryTransaction(store) as transaction:
            transaction.create(pending)
            transaction.delete("existing-record")
            raise RuntimeError("forced failure")

    assert store.get("existing-record") == existing
    assert store.get("pending-record") is None
    assert store.count() == 1


def test_transaction_supports_atomic_multiple_operations(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    first = build_record(
        memory_id="atomic-first",
        content="First original memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    second = build_record(
        memory_id="atomic-second",
        content="Second original memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    third = build_record(
        memory_id="atomic-third",
        content="Third new memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    updated_first = replace(
        first,
        content="First updated memory",
        importance=0.9,
    )

    store.create(first)
    store.create(second)

    with InMemoryTransaction(store) as transaction:
        transaction.update(updated_first)
        transaction.delete("atomic-second")
        transaction.create(third)

    assert store.get("atomic-first") == updated_first
    assert store.get("atomic-second") is None
    assert store.get("atomic-third") == third
    assert store.count() == 2


def test_failed_multi_operation_transaction_is_atomic(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    original = build_record(
        memory_id="atomic-original",
        content="Original state",
        memory_type=memory_type,
        identity=global_identity,
    )
    pending = build_record(
        memory_id="atomic-pending",
        content="Pending state",
        memory_type=memory_type,
        identity=global_identity,
    )
    updated = replace(
        original,
        content="Changed state",
    )

    store.create(original)

    with pytest.raises(ValueError, match="does not exist"):
        with InMemoryTransaction(store) as transaction:
            transaction.update(updated)
            transaction.create(pending)
            transaction.update(
                build_record(
                    memory_id="missing-record",
                    content="Missing memory",
                    memory_type=memory_type,
                    identity=global_identity,
                )
            )

    assert store.get("atomic-original") == original
    assert store.get("atomic-pending") is None
    assert store.count() == 1


def test_transaction_update_persists_on_commit(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    original = build_record(
        memory_id="update-record",
        content="Original content",
        memory_type=memory_type,
        identity=global_identity,
    )
    updated = replace(
        original,
        content="Updated content",
        confidence=0.8,
    )

    store.create(original)

    with InMemoryTransaction(store) as transaction:
        result = transaction.update(updated)

    assert result == updated
    assert store.get("update-record") == updated


def test_transaction_update_rejects_unknown_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    unknown = build_record(
        memory_id="unknown-update",
        content="Unknown memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    with pytest.raises(ValueError, match="does not exist"):
        with InMemoryTransaction(store) as transaction:
            transaction.update(unknown)

    assert store.count() == 0


def test_transaction_create_rejects_duplicate_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    existing = build_record(
        memory_id="duplicate-record",
        content="Existing memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    store.create(existing)

    with pytest.raises(ValueError, match="already exists"):
        with InMemoryTransaction(store) as transaction:
            transaction.create(existing)

    assert store.get("duplicate-record") == existing
    assert store.count() == 1


def test_transaction_delete_persists_on_commit(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    record = build_record(
        memory_id="delete-record",
        content="Delete this memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    store.create(record)

    with InMemoryTransaction(store) as transaction:
        deleted = transaction.delete("delete-record")

    assert deleted is True
    assert store.get("delete-record") is None
    assert store.count() == 0


def test_transaction_delete_unknown_record_returns_false() -> None:
    store = InMemoryStore()

    with InMemoryTransaction(store) as transaction:
        deleted = transaction.delete("missing-record")

    assert deleted is False
    assert store.count() == 0


def test_transaction_clear_persists_on_commit(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    for index in range(3):
        store.create(
            build_record(
                memory_id=f"clear-record-{index}",
                content=f"Clear memory {index}",
                memory_type=memory_type,
                identity=global_identity,
            )
        )

    with InMemoryTransaction(store) as transaction:
        deleted_count = transaction.clear()

    assert deleted_count == 3
    assert store.count() == 0


def test_transaction_clear_is_reverted_by_rollback(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    first = build_record(
        memory_id="rollback-clear-first",
        content="First retained memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    second = build_record(
        memory_id="rollback-clear-second",
        content="Second retained memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    store.create(first)
    store.create(second)

    transaction = InMemoryTransaction(store)
    transaction.__enter__()

    assert transaction.clear() == 2

    transaction.rollback()

    assert store.get("rollback-clear-first") == first
    assert store.get("rollback-clear-second") == second
    assert store.count() == 2


def test_transaction_changes_are_not_visible_before_commit(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    record = build_record(
        memory_id="isolated-record",
        content="Isolated pending memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    transaction = InMemoryTransaction(store)
    transaction.__enter__()
    transaction.create(record)

    assert store._records.get("isolated-record") is None

    transaction.commit()

    assert store.get("isolated-record") == record


def test_operations_require_active_transaction(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    record = build_record(
        memory_id="inactive-record",
        content="Inactive transaction memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    with pytest.raises(RuntimeError, match="not active"):
        transaction.create(record)

    with pytest.raises(RuntimeError, match="not active"):
        transaction.update(record)

    with pytest.raises(RuntimeError, match="not active"):
        transaction.delete("inactive-record")

    with pytest.raises(RuntimeError, match="not active"):
        transaction.clear()

    with pytest.raises(RuntimeError, match="not active"):
        transaction.commit()

    with pytest.raises(RuntimeError, match="not active"):
        transaction.rollback()


def test_transaction_cannot_be_entered_twice_while_active() -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    transaction.__enter__()

    try:
        with pytest.raises(RuntimeError, match="already active"):
            transaction.__enter__()
    finally:
        transaction.rollback()


def test_committed_transaction_cannot_be_reused() -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.commit()

    with pytest.raises(RuntimeError, match="cannot be reused"):
        transaction.__enter__()


def test_rolled_back_transaction_cannot_be_reused() -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.rollback()

    with pytest.raises(RuntimeError, match="cannot be reused"):
        transaction.__enter__()


def test_commit_cannot_be_called_twice() -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.commit()

    with pytest.raises(RuntimeError, match="not active"):
        transaction.commit()


def test_rollback_cannot_be_called_after_commit() -> None:
    store = InMemoryStore()
    transaction = InMemoryTransaction(store)

    transaction.__enter__()
    transaction.commit()

    with pytest.raises(RuntimeError, match="not active"):
        transaction.rollback()


def test_exception_is_not_suppressed(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    record = build_record(
        memory_id="exception-record",
        content="Exception memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    with pytest.raises(KeyError, match="transaction failure"):
        with InMemoryTransaction(store) as transaction:
            transaction.create(record)
            raise KeyError("transaction failure")

    assert store.get("exception-record") is None


def test_store_remains_usable_after_transaction_commit(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    committed = build_record(
        memory_id="committed-record",
        content="Committed memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    direct = build_record(
        memory_id="direct-record",
        content="Directly created memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    with InMemoryTransaction(store) as transaction:
        transaction.create(committed)

    store.create(direct)

    assert store.get("committed-record") == committed
    assert store.get("direct-record") == direct
    assert store.count() == 2


def test_store_remains_usable_after_transaction_rollback(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    rolled_back = build_record(
        memory_id="rolled-back-record",
        content="Rolled-back memory",
        memory_type=memory_type,
        identity=global_identity,
    )
    direct = build_record(
        memory_id="post-rollback-record",
        content="Post-rollback memory",
        memory_type=memory_type,
        identity=global_identity,
    )

    transaction = InMemoryTransaction(store)
    transaction.__enter__()
    transaction.create(rolled_back)
    transaction.rollback()

    store.create(direct)

    assert store.get("rolled-back-record") is None
    assert store.get("post-rollback-record") == direct
    assert store.count() == 1