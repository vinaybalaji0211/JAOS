"""Static context source for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from threading import RLock

from jaos.intelligence.exceptions import (
    IntelligenceComponentStateError,
)
from jaos.intelligence.interfaces import IntelligenceContextSource
from jaos.intelligence.models import ContextItem, IntelligenceRequest


def _normalize_source_name(source_name: str) -> str:
    """Validate and normalize a source name."""

    if not isinstance(source_name, str):
        raise TypeError("source_name must be a string")

    normalized = source_name.strip().lower()

    if not normalized:
        raise ValueError("source_name must not be empty")

    return normalized


class StaticContextSource(IntelligenceContextSource):
    """Provides an immutable collection of approved context items."""

    def __init__(
        self,
        source_name: str,
        items: tuple[ContextItem, ...] = (),
    ) -> None:
        if not isinstance(items, (tuple, list)):
            raise TypeError("items must be a tuple or list")

        if not all(
            isinstance(item, ContextItem)
            for item in items
        ):
            raise TypeError(
                "items must contain ContextItem instances"
            )

        item_ids = [item.item_id for item in items]

        if len(item_ids) != len(set(item_ids)):
            raise ValueError("context source item IDs must be unique")

        self._source_name = _normalize_source_name(source_name)
        self._items = tuple(items)
        self._ready = False
        self._lock = RLock()

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return f"context-source:{self._source_name}"

    @property
    def source_name(self) -> str:
        """Return the stable source name."""

        return self._source_name

    @property
    def is_ready(self) -> bool:
        """Return whether the source can provide context."""

        with self._lock:
            return self._ready

    def initialize(self) -> None:
        """Enable context collection."""

        with self._lock:
            self._ready = True

    def shutdown(self) -> None:
        """Disable context collection."""

        with self._lock:
            self._ready = False

    def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        """Return the source's immutable context items."""

        if not isinstance(request, IntelligenceRequest):
            raise TypeError(
                "request must be an instance of IntelligenceRequest"
            )

        if not self.is_ready:
            raise IntelligenceComponentStateError(
                "static context source is not ready",
                request_id=request.request_id,
                component=self.component_name,
                details={"source_name": self.source_name},
            )

        return self._items