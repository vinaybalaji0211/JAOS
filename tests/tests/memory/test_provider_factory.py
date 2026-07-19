"""
JAOS Memory Platform

Provider Factory Integration Tests

Verifies that SQLite and PostgreSQL providers coexist behind the
provider-independent registry and factory abstractions.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jaos.memory.providers.postgres_provider import (
    PostgreSQLProvider,
)
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)
from jaos.memory.providers.provider_factory import ProviderFactory
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos.memory.storage.memory_store import MemoryStore


POSTGRES_CONNECTION_STRING = (
    "postgresql://jaos:secret@localhost:5432/jaos_test"
)


@pytest.fixture
def sqlite_provider(
    tmp_path: Path,
) -> SQLiteProvider:
    """
    Return an isolated SQLite provider.
    """
    return SQLiteProvider(
        database_path=tmp_path / "memory.db",
    )


@pytest.fixture
def postgres_provider() -> PostgreSQLProvider:
    """
    Return a configured PostgreSQL provider.

    Tests monkeypatch database-dependent methods, so a live
    PostgreSQL server is not required.
    """
    return PostgreSQLProvider(
        connection_string=POSTGRES_CONNECTION_STRING,
    )


@pytest.fixture
def registry() -> ProviderRegistry:
    """
    Return an empty provider registry.
    """
    return ProviderRegistry()


@pytest.fixture
def factory(
    registry: ProviderRegistry,
) -> ProviderFactory:
    """
    Return a provider factory using the empty registry.
    """
    return ProviderFactory(registry)


def test_register_sqlite_and_postgresql_providers(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Both concrete providers can coexist in one registry.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    assert registry.provider_ids() == (
        "postgresql",
        "sqlite",
    )
    assert registry.get("sqlite") is sqlite_provider
    assert (
        registry.get("postgresql")
        is postgres_provider
    )


def test_sqlite_remains_default_provider(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    SQLite remains the default when PostgreSQL is also registered.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(postgres_provider)
    registry.register(sqlite_provider)

    assert registry.default_provider_id == "sqlite"
    assert registry.get_default() is sqlite_provider


def test_postgresql_can_be_selected_as_default(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    PostgreSQL may explicitly become the default provider.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(
        postgres_provider,
        make_default=True,
    )

    assert (
        registry.default_provider_id
        == "postgresql"
    )
    assert (
        registry.get_default()
        is postgres_provider
    )


def test_factory_resolves_both_providers(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    The factory resolves both backends by provider ID.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    factory = ProviderFactory(registry)

    assert (
        factory.resolve_provider("sqlite")
        is sqlite_provider
    )
    assert (
        factory.resolve_provider("postgresql")
        is postgres_provider
    )


def test_factory_lists_both_provider_ids(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    The factory exposes deterministic provider IDs.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    factory = ProviderFactory(registry)

    assert factory.available_provider_ids() == (
        "postgresql",
        "sqlite",
    )


def test_factory_creates_sqlite_store(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    The factory creates a concrete SQLite store.
    """
    registry.register(sqlite_provider)

    factory = ProviderFactory(registry)
    store = factory.create("sqlite")

    try:
        assert isinstance(store, SQLiteStore)
        assert isinstance(store, MemoryStore)
    finally:
        store.close()


def test_factory_creates_default_sqlite_store(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    The default factory path creates SQLite when SQLite is default.
    """
    registry.register(sqlite_provider)

    factory = ProviderFactory(registry)
    store = factory.create_default()

    try:
        assert isinstance(store, SQLiteStore)
        assert isinstance(store, MemoryStore)
    finally:
        store.close()


def test_factory_routes_postgresql_store_creation(
    tmp_path: Path,
    registry: ProviderRegistry,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    The factory delegates PostgreSQL store creation to the
    PostgreSQL provider without requiring a live database.
    """
    fallback_store = SQLiteStore(
        database_path=tmp_path / "postgres-route.db",
    )

    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "health_check",
        lambda: True,
    )
    monkeypatch.setattr(
        postgres_provider,
        "create_store",
        lambda: fallback_store,
    )

    registry.register(postgres_provider)
    factory = ProviderFactory(registry)

    store = factory.create("postgresql")

    try:
        assert store is fallback_store
        assert isinstance(store, MemoryStore)
    finally:
        store.close()


def test_factory_rejects_unhealthy_postgresql_provider(
    registry: ProviderRegistry,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Factory creation fails when PostgreSQL health checking fails.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "health_check",
        lambda: False,
    )

    registry.register(postgres_provider)
    factory = ProviderFactory(registry)

    with pytest.raises(
        RuntimeError,
        match="Memory provider health check failed: postgresql",
    ):
        factory.create("postgresql")


def test_factory_can_skip_postgresql_health_check(
    tmp_path: Path,
    registry: ProviderRegistry,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Explicitly disabling health validation bypasses health_check.
    """
    fallback_store = SQLiteStore(
        database_path=tmp_path / "skip-health.db",
    )

    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "health_check",
        lambda: False,
    )
    monkeypatch.setattr(
        postgres_provider,
        "create_store",
        lambda: fallback_store,
    )

    registry.register(postgres_provider)
    factory = ProviderFactory(registry)

    store = factory.create(
        "postgresql",
        require_healthy=False,
    )

    try:
        assert store is fallback_store
    finally:
        store.close()


@pytest.mark.parametrize(
    "capability",
    (
        ProviderCapability.PERSISTENCE,
        ProviderCapability.TRANSACTIONS,
        ProviderCapability.SEARCH,
        ProviderCapability.FILTERING,
        ProviderCapability.PAGINATION,
        ProviderCapability.SORTING,
        ProviderCapability.BATCH_OPERATIONS,
        ProviderCapability.STATISTICS,
        ProviderCapability.HEALTH_CHECKS,
    ),
)
def test_both_providers_expose_required_capabilities(
    capability: ProviderCapability,
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    SQLite and PostgreSQL expose the same certified capabilities.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    factory = ProviderFactory(registry)

    assert factory.supports(
        capability,
        provider_id="sqlite",
    )
    assert factory.supports(
        capability,
        provider_id="postgresql",
    )


def test_factory_enforces_required_capabilities(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    Required supported capabilities allow store creation.
    """
    registry.register(sqlite_provider)
    factory = ProviderFactory(registry)

    store = factory.create(
        "sqlite",
        required_capabilities=(
            ProviderCapability.PERSISTENCE,
            ProviderCapability.TRANSACTIONS,
            ProviderCapability.SEARCH,
        ),
    )

    try:
        assert isinstance(store, SQLiteStore)
    finally:
        store.close()


def test_registry_finds_both_persistent_providers(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Capability discovery returns both persistent backends.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    matches = registry.find_supporting(
        ProviderCapability.PERSISTENCE
    )

    assert tuple(
        provider.provider_id
        for provider in matches
    ) == (
        "postgresql",
        "sqlite",
    )


def test_registry_finds_both_transactional_providers(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Both backends satisfy combined capability discovery.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    matches = registry.find_supporting_all(
        (
            ProviderCapability.PERSISTENCE,
            ProviderCapability.TRANSACTIONS,
            ProviderCapability.SEARCH,
        )
    )

    assert tuple(
        provider.provider_id
        for provider in matches
    ) == (
        "postgresql",
        "sqlite",
    )


def test_registry_switches_default_between_backends(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Runtime default selection can switch between backends.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    assert registry.default_provider_id == "sqlite"

    registry.set_default("postgresql")

    assert (
        registry.default_provider_id
        == "postgresql"
    )
    assert (
        registry.get_default()
        is postgres_provider
    )

    registry.set_default("sqlite")

    assert registry.default_provider_id == "sqlite"
    assert registry.get_default() is sqlite_provider


def test_unregistering_postgresql_preserves_sqlite(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Removing PostgreSQL does not affect SQLite registration.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "shutdown",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    removed = registry.unregister("postgresql")

    assert removed is postgres_provider
    assert registry.provider_ids() == ("sqlite",)
    assert registry.get_default() is sqlite_provider


def test_unregistering_default_selects_remaining_backend(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Removing the default provider selects the remaining provider.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "shutdown",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(
        postgres_provider,
        make_default=True,
    )

    assert (
        registry.default_provider_id
        == "postgresql"
    )

    registry.unregister("postgresql")

    assert registry.default_provider_id == "sqlite"
    assert registry.get_default() is sqlite_provider


def test_registry_clear_removes_both_backends(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
    postgres_provider: PostgreSQLProvider,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Clearing the registry removes both providers.
    """
    monkeypatch.setattr(
        postgres_provider,
        "initialize",
        lambda: None,
    )
    monkeypatch.setattr(
        postgres_provider,
        "shutdown",
        lambda: None,
    )

    registry.register(sqlite_provider)
    registry.register(postgres_provider)

    removed_count = registry.clear()

    assert removed_count == 2
    assert registry.provider_ids() == ()
    assert registry.default_provider_id is None
    assert len(registry) == 0


def test_unknown_provider_is_rejected(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    Unknown provider IDs fail deterministically.
    """
    registry.register(sqlite_provider)
    factory = ProviderFactory(registry)

    with pytest.raises(
        KeyError,
        match="Memory provider is not registered: unknown",
    ):
        factory.create("unknown")


def test_empty_provider_id_is_rejected(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    Empty provider IDs are invalid.
    """
    registry.register(sqlite_provider)
    factory = ProviderFactory(registry)

    with pytest.raises(
        ValueError,
        match="provider_id must not be empty",
    ):
        factory.create("   ")


def test_non_string_provider_id_is_rejected(
    registry: ProviderRegistry,
    sqlite_provider: SQLiteProvider,
) -> None:
    """
    Provider IDs must be strings or None.
    """
    registry.register(sqlite_provider)
    factory = ProviderFactory(registry)

    with pytest.raises(
        TypeError,
        match="provider_id must be a string or None",
    ):
        factory.create(123)  # type: ignore[arg-type]