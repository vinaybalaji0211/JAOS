from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from logs.logger import logger


class EventBus:
    """Simple publish/subscribe event bus for JAOS."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable) -> None:
        self._subscribers[event].append(handler)
        logger.debug("Subscribed handler to event: %s", event)

    def publish(self, event: str, payload=None) -> None:
        logger.debug("Publishing event: %s", event)

        for handler in self._subscribers.get(event, []):
            handler(payload)

    def subscriber_count(self, event: str) -> int:
        return len(self._subscribers.get(event, []))

    def clear(self) -> None:
        self._subscribers.clear()