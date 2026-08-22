from __future__ import annotations

from jaos_platform.runtime_paths import RuntimePaths
from logs.logger import logger


class RuntimeContext:
    """Shared runtime state for the JAOS platform."""

    def __init__(
        self,
        *,
        runtime_paths: RuntimePaths | None = None,
    ) -> None:
        self._runtime_paths = runtime_paths
        self._context: dict[str, object] = {}

    @property
    def runtime_paths(self) -> RuntimePaths | None:
        """Return the canonical paths supplied by the composition owner."""

        return self._runtime_paths

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
