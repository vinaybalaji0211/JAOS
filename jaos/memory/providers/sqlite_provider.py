"""
JAOS Memory Platform

SQLite Memory Provider

Concrete MemoryProvider implementation backed by SQLiteStore.
"""

from __future__ import annotations

from pathlib import Path

from jaos.memory.providers.database_constants import (
    DEFAULT_DATABASE_FILENAME,
)
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
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos.memory.storage.memory_store import MemoryStore


class SQLiteProvider(MemoryProvider):
    """
    SQLite-backed implementation of MemoryProvider.
    """

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        """
        Initialize the SQLite provider.

        Args:
            database_path:
                Absolute SQLite database file path. Relative paths are
                rejected so provider state cannot resolve against the
                current working directory.
        """
        try:
            normalized_path = Path(database_path)

        except (TypeError, ValueError, OSError) as error:
            raise ValueError(
                "database_path must be a valid absolute path"
            ) from error

        if not normalized_path.is_absolute():
            raise ValueError(
                "database_path must be an absolute path"
            )

        self._database_path = normalized_path

        self._descriptor = ProviderDescriptor(
            provider_id="sqlite",
            provider_name="SQLite Memory Provider",
            provider_version="1.0",
            description=(
                "SQLite-based persistent memory provider."
            ),
            author="JAOS",
            supports_persistence=True,
            is_default=True,
            capabilities=ProviderCapabilities.from_iterable(
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
            ),
        )

    @classmethod
    def from_memory_scope(
        cls,
        memory_scope: str | Path,
    ) -> SQLiteProvider:
        """Create a provider bound to an injected runtime memory scope."""
        try:
            normalized_scope = Path(memory_scope)
        except (TypeError, ValueError, OSError) as error:
            raise ValueError(
                "memory_scope must be a valid absolute path"
            ) from error

        if not normalized_scope.is_absolute():
            raise ValueError(
                "memory_scope must be an absolute path"
            )

        return cls(
            database_path=(
                normalized_scope / DEFAULT_DATABASE_FILENAME
            ),
        )

    @property
    def descriptor(self) -> ProviderDescriptor:
        """
        Return provider metadata.
        """
        return self._descriptor

    @property
    def database_path(self) -> Path:
        """
        Return the configured SQLite database path.
        """
        return self._database_path

    def create_store(self) -> MemoryStore:
        """
        Create a SQLiteStore instance.
        """
        return SQLiteStore(
            database_path=self._database_path,
        )

    def initialize(self) -> None:
        """
        Ensure the database parent directory exists.
        """
        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def shutdown(self) -> None:
        """
        SQLite requires no provider-level shutdown.
        """

    def health_check(self) -> bool:
        """
        Return whether the provider configuration is valid.
        """
        return (
            self._database_path.parent.exists()
            and self._database_path.parent.is_dir()
        )

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.
        """
        return (
            "SQLiteProvider("
            f"database_path={self._database_path})"
        )
