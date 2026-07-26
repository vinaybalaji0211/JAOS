"""Context source registry for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from threading import RLock

from jaos.intelligence.exceptions import IntelligenceContextError
from jaos.intelligence.interfaces import IntelligenceContextSource


def _normalize_source_name(source_name: str) -> str:
    """Validate and normalize a context-source name."""

    if not isinstance(source_name, str):
        raise TypeError("source_name must be a string")

    normalized = source_name.strip().lower()

    if not normalized:
        raise ValueError("source_name must not be empty")

    return normalized


class ContextSourceRegistry:
    """
    Thread-safe registry of provider-independent context sources.

    The registry owns source discovery only. Context collection,
    filtering, ranking, and token-budget enforcement remain the
    responsibility of the Intelligence Context Manager.
    """

    def __init__(self) -> None:
        self._sources: dict[str, IntelligenceContextSource] = {}
        self._lock = RLock()

    def register_source(
        self,
        source: IntelligenceContextSource,
    ) -> None:
        """Register a unique context source."""

        if not isinstance(source, IntelligenceContextSource):
            raise TypeError(
                "source must implement IntelligenceContextSource"
            )

        source_name = _normalize_source_name(source.source_name)

        with self._lock:
            if source_name in self._sources:
                raise IntelligenceContextError(
                    f"context source already registered: {source_name}",
                    details={"source_name": source_name},
                )

            self._sources[source_name] = source

    def unregister_source(
        self,
        source_name: str,
    ) -> IntelligenceContextSource:
        """Remove and return a registered context source."""

        normalized_name = _normalize_source_name(source_name)

        with self._lock:
            source = self._sources.pop(normalized_name, None)

        if source is None:
            raise IntelligenceContextError(
                f"context source not found: {normalized_name}",
                details={"source_name": normalized_name},
            )

        return source

    def get_source(
        self,
        source_name: str,
    ) -> IntelligenceContextSource:
        """Return a registered context source."""

        normalized_name = _normalize_source_name(source_name)

        with self._lock:
            source = self._sources.get(normalized_name)

        if source is None:
            raise IntelligenceContextError(
                f"context source not found: {normalized_name}",
                details={"source_name": normalized_name},
            )

        return source

    def list_sources(self) -> tuple[IntelligenceContextSource, ...]:
        """Return all registered sources in registration order."""

        with self._lock:
            return tuple(self._sources.values())

    def contains(self, source_name: str) -> bool:
        """Return whether a source name is registered."""

        normalized_name = _normalize_source_name(source_name)

        with self._lock:
            return normalized_name in self._sources

    def clear(self) -> None:
        """Remove all context source registrations."""

        with self._lock:
            self._sources.clear()

    def __len__(self) -> int:
        """Return the number of registered context sources."""

        with self._lock:
            return len(self._sources)