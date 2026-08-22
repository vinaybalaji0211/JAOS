from __future__ import annotations

"""
Database configuration shared by memory storage providers.

This module centralizes provider-independent database configuration
used throughout the JAOS Memory Platform.

SQLite uses these values today.

Future providers (PostgreSQL, pgvector, Cloud Memory Platform)
should reuse applicable values to maintain consistent behavior.
"""

###############################################################################
# Schema
###############################################################################

SCHEMA_VERSION = 1

###############################################################################
# Database
###############################################################################

DEFAULT_DATABASE_FILENAME = "memory.sqlite3"

###############################################################################
# SQLite Configuration
###############################################################################

SQLITE_BUSY_TIMEOUT_MS = 5000

SQLITE_CACHE_SIZE = -20000

SQLITE_PAGE_SIZE = 4096

SQLITE_JOURNAL_MODE = "WAL"

SQLITE_SYNCHRONOUS = "NORMAL"

SQLITE_TEMP_STORE = "MEMORY"

SQLITE_FOREIGN_KEYS = True

###############################################################################
# Search
###############################################################################

DEFAULT_SEARCH_LIMIT = 100

MAX_SEARCH_LIMIT = 1000

###############################################################################
# Future Cloud Memory Platform
###############################################################################

DEFAULT_VECTOR_DIMENSION = 1536

DEFAULT_EMBEDDING_PROVIDER = "openai"

###############################################################################
# Storage Tiers
###############################################################################

HOT_STORAGE = "hot"

WARM_STORAGE = "warm"

COLD_STORAGE = "cold"

TEMPORARY_STORAGE = "temporary"

RESTRICTED_STORAGE = "restricted"
