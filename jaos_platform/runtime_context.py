from __future__ import annotations

from logs.logger import logger


class RuntimeContext:
    """Shared runtime state for the JAOS platform."""

    def __init__(self) -> None:
        self._context: dict[str, object] = {}

    def set(self, key: str, value: object) -> None:
        self._context[key] = value
        logger.debug("RuntimeContext set: %s", key)

    def get(self, key: str, default: object = None) -> object:
        return self._context.get(key, default)

    def remove(self, key: str) -> None:
        self._context.pop(key, None)

    def contains(self, key: str) -> bool:
        return key in self._context

    def clear(self) -> None:
        self._context.clear()

    def keys(self) -> list[str]:
        return sorted(self._context.keys())