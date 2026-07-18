"""
JAOS Memory Platform

Provider Capability Definitions

Each MemoryStore implementation advertises its supported
features through these capabilities.

This allows higher-level components to remain completely
provider-independent.
"""

from __future__ import annotations

from enum import StrEnum


class ProviderCapability(StrEnum):
    """
    Capabilities that may be supported by a memory provider.
    """

    PERSISTENCE = "persistence"

    TRANSACTIONS = "transactions"

    SEARCH = "search"

    FILTERING = "filtering"

    PAGINATION = "pagination"

    SORTING = "sorting"

    SEMANTIC_SEARCH = "semantic_search"

    VECTOR_SEARCH = "vector_search"

    EMBEDDINGS = "embeddings"

    SNAPSHOTS = "snapshots"

    VERSIONING = "versioning"

    ENCRYPTION = "encryption"

    COMPRESSION = "compression"

    CLOUD_SYNC = "cloud_sync"

    REPLICATION = "replication"

    MIGRATION = "migration"

    BACKUPS = "backups"

    AUDITING = "auditing"

    ACCESS_CONTROL = "access_control"

    METADATA_INDEXING = "metadata_indexing"

    FULL_TEXT_SEARCH = "full_text_search"

    STREAMING = "streaming"

    BATCH_OPERATIONS = "batch_operations"

    STATISTICS = "statistics"

    HEALTH_CHECKS = "health_checks"