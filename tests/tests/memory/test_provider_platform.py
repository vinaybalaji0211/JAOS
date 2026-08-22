"""
JAOS Memory Platform

Provider Platform Certification Tests

Certifies:
- ProviderCapabilities
- ProviderDescriptor
- MemoryProvider
- ProviderRegistry
- ProviderFactory
- SQLiteProvider
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jaos.memory.providers.memory_provider import MemoryProvider
from jaos.memory.providers.provider_capabilities import (
    ProviderCapabilities,
)
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)
from jaos.memory.providers.provider_descriptor import (
    ProviderDescriptor,
)
from jaos.memory.providers.provider_factory import ProviderFactory
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos.memory.storage.memory_store import MemoryStore


class TestProviderCapabilities:
    """
    Certify provider capability collections.
    """

    def test_empty_capabilities(self) -> None:
        capabilities = ProviderCapabilities.empty()

        assert len(capabilities) == 0
        assert not capabilities
        assert capabilities.to_sorted_tuple() == ()

    def test_create_from_iterable(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (
                ProviderCapability.PERSISTENCE,
                ProviderCapability.TRANSACTIONS,
            )
        )

        assert len(capabilities) == 2
        assert ProviderCapability.PERSISTENCE in capabilities
        assert ProviderCapability.TRANSACTIONS in capabilities

    def test_capabilities_are_immutable(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.PERSISTENCE,)
        )

        with pytest.raises(AttributeError):
            capabilities.values = frozenset()

    def test_duplicate_capabilities_are_removed(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (
                ProviderCapability.PERSISTENCE,
                ProviderCapability.PERSISTENCE,
            )
        )

        assert len(capabilities) == 1

    def test_supports(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.SEARCH,)
        )

        assert capabilities.supports(
            ProviderCapability.SEARCH
        )
        assert not capabilities.supports(
            ProviderCapability.VECTOR_SEARCH
        )

    def test_supports_all(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.FILTERING,
            )
        )

        assert capabilities.supports_all(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.FILTERING,
            )
        )

        assert not capabilities.supports_all(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.VECTOR_SEARCH,
            )
        )

    def test_supports_any(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.SEARCH,)
        )

        assert capabilities.supports_any(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.VECTOR_SEARCH,
            )
        )

        assert not capabilities.supports_any(
            (
                ProviderCapability.ENCRYPTION,
                ProviderCapability.VECTOR_SEARCH,
            )
        )

    def test_missing_capabilities(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.SEARCH,)
        )

        missing = capabilities.missing(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.ENCRYPTION,
            )
        )

        assert missing == frozenset(
            (ProviderCapability.ENCRYPTION,)
        )

    def test_require_supported_capability(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.PERSISTENCE,)
        )

        capabilities.require(
            ProviderCapability.PERSISTENCE
        )

    def test_require_unsupported_capability(self) -> None:
        capabilities = ProviderCapabilities.empty()

        with pytest.raises(
            RuntimeError,
            match="persistence",
        ):
            capabilities.require(
                ProviderCapability.PERSISTENCE
            )

    def test_require_all_unsupported_capabilities(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (ProviderCapability.PERSISTENCE,)
        )

        with pytest.raises(RuntimeError):
            capabilities.require_all(
                (
                    ProviderCapability.PERSISTENCE,
                    ProviderCapability.ENCRYPTION,
                    ProviderCapability.VECTOR_SEARCH,
                )
            )

    def test_iteration_is_deterministic(self) -> None:
        capabilities = ProviderCapabilities.from_iterable(
            (
                ProviderCapability.TRANSACTIONS,
                ProviderCapability.PERSISTENCE,
                ProviderCapability.SEARCH,
            )
        )

        values = [
            capability.value
            for capability in capabilities
        ]

        assert values == sorted(values)

    @pytest.mark.parametrize(
        "invalid",
        [
            "persistence",
            123,
            object(),
            None,
        ],
    )
    def test_invalid_single_capability(
        self,
        invalid: object,
    ) -> None:
        capabilities = ProviderCapabilities.empty()

        with pytest.raises(TypeError):
            capabilities.supports(invalid)

    def test_invalid_capability_collection_string(self) -> None:
        with pytest.raises(TypeError):
            ProviderCapabilities.from_iterable(
                "persistence"
            )

    def test_invalid_capability_collection_member(self) -> None:
        with pytest.raises(TypeError):
            ProviderCapabilities.from_iterable(
                (
                    ProviderCapability.PERSISTENCE,
                    "transactions",
                )
            )


class TestProviderDescriptor:
    """
    Certify provider descriptors.
    """

    def test_valid_descriptor(self) -> None:
        descriptor = ProviderDescriptor(
            provider_id="test",
            provider_name="Test Provider",
            provider_version="1.0",
            capabilities=ProviderCapabilities.empty(),
        )

        assert descriptor.provider_id == "test"
        assert descriptor.provider_name == "Test Provider"
        assert descriptor.provider_version == "1.0"
        assert descriptor.author == "JAOS"
        assert descriptor.supports_persistence
        assert not descriptor.is_default

    def test_capability_count(self) -> None:
        descriptor = ProviderDescriptor(
            provider_id="test",
            provider_name="Test Provider",
            provider_version="1.0",
            capabilities=ProviderCapabilities.from_iterable(
                (
                    ProviderCapability.PERSISTENCE,
                    ProviderCapability.SEARCH,
                )
            ),
        )

        assert descriptor.capability_count == 2

    def test_descriptor_supports_capability(self) -> None:
        descriptor = ProviderDescriptor(
            provider_id="test",
            provider_name="Test Provider",
            provider_version="1.0",
            capabilities=ProviderCapabilities.from_iterable(
                (ProviderCapability.SEARCH,)
            ),
        )

        assert descriptor.supports(
            ProviderCapability.SEARCH
        )

    @pytest.mark.parametrize(
        ("field_name", "value"),
        [
            ("provider_id", ""),
            ("provider_id", "   "),
            ("provider_name", ""),
            ("provider_version", ""),
        ],
    )
    def test_empty_required_descriptor_fields(
        self,
        field_name: str,
        value: str,
    ) -> None:
        values = {
            "provider_id": "test",
            "provider_name": "Test Provider",
            "provider_version": "1.0",
            "capabilities": ProviderCapabilities.empty(),
        }

        values[field_name] = value

        with pytest.raises(ValueError):
            ProviderDescriptor(**values)

    def test_invalid_capabilities_type(self) -> None:
        with pytest.raises(TypeError):
            ProviderDescriptor(
                provider_id="test",
                provider_name="Test Provider",
                provider_version="1.0",
                capabilities=frozenset(),
            )


class FakeProvider(MemoryProvider):
    """
    Test provider used to certify registry and factory behavior.
    """

    def __init__(
        self,
        provider_id: str,
        *,
        capabilities: tuple[
            ProviderCapability,
            ...,
        ] = (),
        healthy: bool = True,
        default: bool = False,
    ) -> None:
        self.initialized = False
        self.shutdown_called = False
        self.healthy = healthy
        self.created_store: MemoryStore | None = None

        self._descriptor = ProviderDescriptor(
            provider_id=provider_id,
            provider_name=f"{provider_id} provider",
            provider_version="1.0",
            capabilities=ProviderCapabilities.from_iterable(
                capabilities
            ),
            is_default=default,
        )

    @property
    def descriptor(self) -> ProviderDescriptor:
        return self._descriptor

    def create_store(self) -> MemoryStore:
        if self.created_store is None:
            raise RuntimeError(
                "FakeProvider store has not been configured"
            )

        return self.created_store

    def initialize(self) -> None:
        self.initialized = True

    def shutdown(self) -> None:
        self.shutdown_called = True

    def health_check(self) -> bool:
        return self.healthy


class InvalidStoreProvider(FakeProvider):
    """
    Provider that intentionally returns an invalid store.
    """

    def create_store(self) -> MemoryStore:
        return object()


class BareMemoryProvider(MemoryProvider):
    """
    Minimal provider that does not override health_check.
    """

    def __init__(self, provider_id: str) -> None:
        self._descriptor = ProviderDescriptor(
            provider_id=provider_id,
            provider_name=f"{provider_id} provider",
            provider_version="1.0",
            capabilities=ProviderCapabilities.from_iterable(()),
        )

    @property
    def descriptor(self) -> ProviderDescriptor:
        return self._descriptor

    def create_store(self) -> MemoryStore:
        raise NotImplementedError


def test_default_health_check_is_unhealthy_until_overridden() -> None:
    provider = BareMemoryProvider("bare")

    assert provider.health_check() is False


class TestProviderRegistry:
    """
    Certify provider registry behavior.
    """

    def test_empty_registry(self) -> None:
        registry = ProviderRegistry()

        assert len(registry) == 0
        assert not registry
        assert registry.default_provider_id is None
        assert registry.provider_ids() == ()

    def test_register_provider(self) -> None:
        registry = ProviderRegistry()
        provider = FakeProvider("alpha")

        registry.register(provider)

        assert len(registry) == 1
        assert provider.initialized
        assert registry.get("alpha") is provider
        assert registry.default_provider_id == "alpha"

    def test_register_duplicate_provider_fails(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("alpha"))

        with pytest.raises(ValueError):
            registry.register(FakeProvider("alpha"))

    def test_replace_provider(self) -> None:
        registry = ProviderRegistry()

        first = FakeProvider("alpha")
        second = FakeProvider("alpha")

        registry.register(first)
        registry.register(second, replace=True)

        assert first.shutdown_called
        assert registry.get("alpha") is second
        assert second.initialized

    def test_make_default_provider(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("alpha"))
        registry.register(
            FakeProvider("beta"),
            make_default=True,
        )

        assert registry.default_provider_id == "beta"
        assert registry.get_default().provider_id == "beta"

    def test_descriptor_default_provider(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("alpha"))
        registry.register(
            FakeProvider(
                "beta",
                default=True,
            )
        )

        assert registry.default_provider_id == "beta"

    def test_set_default_provider(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("alpha"))
        registry.register(FakeProvider("beta"))

        registry.set_default("beta")

        assert registry.get_default().provider_id == "beta"

    def test_set_unknown_default_fails(self) -> None:
        registry = ProviderRegistry()

        with pytest.raises(KeyError):
            registry.set_default("missing")

    def test_get_unknown_provider_fails(self) -> None:
        registry = ProviderRegistry()

        with pytest.raises(KeyError):
            registry.get("missing")

    def test_optional_lookup(self) -> None:
        registry = ProviderRegistry()

        provider = FakeProvider("alpha")
        registry.register(provider)

        assert registry.get_optional("alpha") is provider
        assert registry.get_optional("missing") is None

    def test_contains_provider(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("alpha"))

        assert registry.contains("alpha")
        assert "alpha" in registry
        assert "missing" not in registry
        assert 123 not in registry

    def test_unregister_provider(self) -> None:
        registry = ProviderRegistry()

        provider = FakeProvider("alpha")
        registry.register(provider)

        removed = registry.unregister("alpha")

        assert removed is provider
        assert provider.shutdown_called
        assert len(registry) == 0
        assert registry.default_provider_id is None

    def test_unregister_unknown_provider(self) -> None:
        registry = ProviderRegistry()

        assert registry.unregister("missing") is None

    def test_unregister_default_selects_next(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("beta"))
        registry.register(FakeProvider("alpha"))
        registry.set_default("beta")

        registry.unregister("beta")

        assert registry.default_provider_id == "alpha"

    def test_provider_listing_is_deterministic(self) -> None:
        registry = ProviderRegistry()

        registry.register(FakeProvider("charlie"))
        registry.register(FakeProvider("alpha"))
        registry.register(FakeProvider("beta"))

        assert registry.provider_ids() == (
            "alpha",
            "beta",
            "charlie",
        )

        assert [
            provider.provider_id
            for provider in registry
        ] == [
            "alpha",
            "beta",
            "charlie",
        ]

    def test_find_supporting_capability(self) -> None:
        registry = ProviderRegistry()

        registry.register(
            FakeProvider(
                "search",
                capabilities=(
                    ProviderCapability.SEARCH,
                ),
            )
        )

        registry.register(
            FakeProvider(
                "vector",
                capabilities=(
                    ProviderCapability.SEARCH,
                    ProviderCapability.VECTOR_SEARCH,
                ),
            )
        )

        matches = registry.find_supporting(
            ProviderCapability.VECTOR_SEARCH
        )

        assert [
            provider.provider_id
            for provider in matches
        ] == ["vector"]

    def test_find_supporting_all_capabilities(self) -> None:
        registry = ProviderRegistry()

        registry.register(
            FakeProvider(
                "basic",
                capabilities=(
                    ProviderCapability.SEARCH,
                ),
            )
        )

        registry.register(
            FakeProvider(
                "advanced",
                capabilities=(
                    ProviderCapability.SEARCH,
                    ProviderCapability.FILTERING,
                ),
            )
        )

        matches = registry.find_supporting_all(
            (
                ProviderCapability.SEARCH,
                ProviderCapability.FILTERING,
            )
        )

        assert [
            provider.provider_id
            for provider in matches
        ] == ["advanced"]

    def test_healthy_providers(self) -> None:
        registry = ProviderRegistry()

        registry.register(
            FakeProvider(
                "healthy",
                healthy=True,
            )
        )

        registry.register(
            FakeProvider(
                "unhealthy",
                healthy=False,
            )
        )

        assert [
            provider.provider_id
            for provider in registry.healthy_providers()
        ] == ["healthy"]

    def test_clear_registry(self) -> None:
        registry = ProviderRegistry()

        first = FakeProvider("alpha")
        second = FakeProvider("beta")

        registry.register(first)
        registry.register(second)

        removed_count = registry.clear()

        assert removed_count == 2
        assert first.shutdown_called
        assert second.shutdown_called
        assert len(registry) == 0
        assert registry.default_provider_id is None

    def test_clear_registry_continues_after_individual_shutdown_failure(
        self,
    ) -> None:
        registry = ProviderRegistry()

        first = FakeProvider("alpha")
        second = FakeProvider("beta")

        def broken_shutdown() -> None:
            raise RuntimeError("alpha shutdown exploded")

        first.shutdown = broken_shutdown

        registry.register(first)
        registry.register(second)

        with pytest.raises(RuntimeError, match="alpha"):
            registry.clear()

        assert second.shutdown_called
        assert len(registry) == 0
        assert registry.default_provider_id is None

    def test_invalid_provider_registration(self) -> None:
        registry = ProviderRegistry()

        with pytest.raises(TypeError):
            registry.register(object())

    @pytest.mark.parametrize(
        "invalid",
        [
            "",
            "   ",
        ],
    )
    def test_invalid_provider_id(
        self,
        invalid: str,
    ) -> None:
        registry = ProviderRegistry()

        with pytest.raises(ValueError):
            registry.get(invalid)


class TestSQLiteProvider:
    """
    Certify SQLite provider integration.
    """

    def test_descriptor(self, tmp_path: Path) -> None:
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        descriptor = provider.descriptor

        assert descriptor.provider_id == "sqlite"
        assert (
            descriptor.provider_name
            == "SQLite Memory Provider"
        )
        assert descriptor.provider_version == "1.0"
        assert descriptor.is_default
        assert descriptor.supports_persistence

    def test_advertised_capabilities(
        self,
        tmp_path: Path,
    ) -> None:
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        expected = (
            ProviderCapability.PERSISTENCE,
            ProviderCapability.TRANSACTIONS,
            ProviderCapability.SEARCH,
            ProviderCapability.FILTERING,
            ProviderCapability.PAGINATION,
            ProviderCapability.SORTING,
            ProviderCapability.BATCH_OPERATIONS,
            ProviderCapability.STATISTICS,
            ProviderCapability.HEALTH_CHECKS,
        )

        assert provider.capabilities.supports_all(
            expected
        )

        assert not provider.supports(
            ProviderCapability.VECTOR_SEARCH
        )

    def test_initialize_creates_parent_directory(
        self,
        tmp_path: Path,
    ) -> None:
        database_path = (
            tmp_path
            / "nested"
            / "storage"
            / "memory.db"
        )

        provider = SQLiteProvider(database_path)

        assert not database_path.parent.exists()

        provider.initialize()

        assert database_path.parent.exists()
        assert database_path.parent.is_dir()

    def test_health_check(
        self,
        tmp_path: Path,
    ) -> None:
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        provider.initialize()

        assert provider.health_check()

    def test_create_store(
        self,
        tmp_path: Path,
    ) -> None:
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        provider.initialize()
        store = provider.create_store()

        try:
            assert isinstance(store, SQLiteStore)
            assert isinstance(store, MemoryStore)
        finally:
            store.close()

    def test_repr_contains_database_path(
        self,
        tmp_path: Path,
    ) -> None:
        database_path = tmp_path / "memory.db"
        provider = SQLiteProvider(database_path)

        representation = repr(provider)

        assert "SQLiteProvider" in representation
        assert str(database_path) in representation


class TestProviderFactory:
    """
    Certify provider factory behavior.
    """

    def test_factory_requires_registry(self) -> None:
        with pytest.raises(TypeError):
            ProviderFactory(object())

    def test_resolve_default_provider(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        assert factory.resolve_provider() is provider

    def test_resolve_provider_by_id(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        assert (
            factory.resolve_provider("sqlite")
            is provider
        )

    def test_create_default_store(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)
        store = factory.create_default()

        try:
            assert isinstance(store, SQLiteStore)
            assert isinstance(store, MemoryStore)
        finally:
            store.close()

    def test_create_store_by_provider_id(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)
        store = factory.create("sqlite")

        try:
            assert isinstance(store, SQLiteStore)
        finally:
            store.close()

    def test_required_capability_supported(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)
        store = factory.create(
            required_capabilities=(
                ProviderCapability.PERSISTENCE,
                ProviderCapability.TRANSACTIONS,
            )
        )

        store.close()

    def test_required_capability_unsupported(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        with pytest.raises(RuntimeError):
            factory.create(
                required_capabilities=(
                    ProviderCapability.VECTOR_SEARCH,
                )
            )

    def test_factory_supports(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()
        provider = SQLiteProvider(
            tmp_path / "memory.db"
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        assert factory.supports(
            ProviderCapability.PERSISTENCE
        )

        assert not factory.supports(
            ProviderCapability.VECTOR_SEARCH
        )

    def test_available_provider_ids(
        self,
        tmp_path: Path,
    ) -> None:
        registry = ProviderRegistry()

        registry.register(
            SQLiteProvider(
                tmp_path / "memory.db"
            )
        )

        factory = ProviderFactory(registry)

        assert factory.available_provider_ids() == (
            "sqlite",
        )

    def test_unhealthy_provider_is_rejected(self) -> None:
        registry = ProviderRegistry()
        provider = FakeProvider(
            "unhealthy",
            healthy=False,
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        with pytest.raises(
            RuntimeError,
            match="health check failed",
        ):
            factory.create()

    def test_health_check_can_be_skipped(self) -> None:
        registry = ProviderRegistry()
        provider = FakeProvider(
            "unhealthy",
            healthy=False,
        )

        registry.register(provider)

        factory = ProviderFactory(registry)

        with pytest.raises(
            RuntimeError,
            match="store has not been configured",
        ):
            factory.create(
                require_healthy=False
            )

    def test_invalid_store_is_rejected(self) -> None:
        registry = ProviderRegistry()
        provider = InvalidStoreProvider("invalid")

        registry.register(provider)

        factory = ProviderFactory(registry)

        with pytest.raises(
            RuntimeError,
            match="invalid store",
        ):
            factory.create()

    def test_no_default_provider(self) -> None:
        factory = ProviderFactory(
            ProviderRegistry()
        )

        with pytest.raises(
            RuntimeError,
            match="No default memory provider",
        ):
            factory.create_default()

    def test_unknown_provider(self) -> None:
        factory = ProviderFactory(
            ProviderRegistry()
        )

        with pytest.raises(KeyError):
            factory.create("missing")

    @pytest.mark.parametrize(
        "invalid",
        [
            "",
            "   ",
        ],
    )
    def test_invalid_provider_id(
        self,
        invalid: str,
    ) -> None:
        factory = ProviderFactory(
            ProviderRegistry()
        )

        with pytest.raises(ValueError):
            factory.resolve_provider(invalid)

    def test_invalid_required_capabilities(self) -> None:
        factory = ProviderFactory(
            ProviderRegistry()
        )

        with pytest.raises(TypeError):
            factory.create(
                required_capabilities="persistence"
            )