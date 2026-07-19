"""
JAOS Memory Platform

PostgreSQL Memory Provider

Concrete MemoryProvider implementation backed by PostgreSQLStore.
"""

from __future__ import annotations

from jaos.memory.providers.memory_provider import MemoryProvider
from jaos.memory.providers.postgres_store import PostgreSQLStore
from jaos.memory.providers.provider_capabilities import (
    ProviderCapabilities,
)
from jaos.memory.providers.provider_capability import (
    ProviderCapability,
)
from jaos.memory.providers.provider_descriptor import (
    ProviderDescriptor,
)
from jaos.memory.storage.memory_store import MemoryStore


class PostgreSQLProvider(MemoryProvider):
    """
    PostgreSQL-backed implementation of MemoryProvider.
    """

    def __init__(
        self,
        connection_string: str,
    ) -> None:
        """
        Initialize the PostgreSQL provider.

        Args:
            connection_string:
                Psycopg-compatible PostgreSQL connection string.

        Raises:
            TypeError:
                If connection_string is not a string.
            ValueError:
                If connection_string is empty.
        """
        if not isinstance(connection_string, str):
            raise TypeError(
                "connection_string must be a string"
            )

        normalized_connection_string = (
            connection_string.strip()
        )

        if not normalized_connection_string:
            raise ValueError(
                "connection_string must not be empty"
            )

        self._connection_string = (
            normalized_connection_string
        )

        self._descriptor = ProviderDescriptor(
            provider_id="postgresql",
            provider_name=(
                "PostgreSQL Memory Provider"
            ),
            provider_version="1.0",
            description=(
                "PostgreSQL-based persistent memory "
                "provider."
            ),
            author="JAOS",
            supports_persistence=True,
            is_default=False,
            capabilities=(
                ProviderCapabilities.from_iterable(
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
                    )
                )
            ),
        )

    @property
    def descriptor(self) -> ProviderDescriptor:
        """
        Return provider metadata.
        """
        return self._descriptor

    @property
    def connection_string(self) -> str:
        """
        Return the configured PostgreSQL connection string.
        """
        return self._connection_string

    def create_store(self) -> MemoryStore:
        """
        Create a PostgreSQLStore instance.
        """
        return PostgreSQLStore(
            connection_string=self._connection_string,
        )

    def initialize(self) -> None:
        """
        Validate PostgreSQL connectivity and initialize schema.

        PostgreSQLStore performs schema initialization during
        construction. Opening and closing a temporary store confirms
        that the configured database is reachable and ready.
        """
        store = self.create_store()
        store.close()

    def shutdown(self) -> None:
        """
        PostgreSQL requires no provider-level shutdown.

        Individual PostgreSQLStore instances own and close their
        database connections.
        """

    def health_check(self) -> bool:
        """
        Return whether PostgreSQL is reachable and operational.
        """
        try:
            store = self.create_store()

            try:
                store.count()
            finally:
                store.close()

        except Exception:
            return False

        return True

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.

        The connection string is intentionally omitted because it may
        contain database credentials.
        """
        return "PostgreSQLProvider(configured=True)"