"""JAOS logging with explicit RuntimePaths-owned file configuration."""

from __future__ import annotations

import logging
from pathlib import Path
from threading import RLock

from jaos_platform.runtime_paths import RuntimePaths


LOGGER_NAME = "JARVIS_OS"
SYSTEM_LOG_FILENAME = "system.log"

_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
_OWNED_HANDLER_ATTRIBUTE = "_jaos_runtime_owned"
_CONFIGURATION_LOCK = RLock()

logger = logging.getLogger(LOGGER_NAME)
_INITIAL_LOGGER_LEVEL = logger.level
_INITIAL_LOGGER_PROPAGATE = logger.propagate


def _is_jaos_owned(handler: logging.Handler) -> bool:
    return bool(getattr(handler, _OWNED_HANDLER_ATTRIBUTE, False))


def _close_jaos_handler(handler: logging.Handler) -> None:
    logger.removeHandler(handler)
    try:
        handler.flush()
    finally:
        handler.close()


def configure_runtime_logging(
    runtime_paths: RuntimePaths,
    *,
    level: int = logging.INFO,
) -> Path:
    """Configure one JAOS file handler beneath the injected logs scope."""

    if not isinstance(runtime_paths, RuntimePaths):
        raise TypeError("runtime_paths must be a RuntimePaths instance")

    logs_directory = runtime_paths.logs
    log_file = logs_directory / SYSTEM_LOG_FILENAME

    with _CONFIGURATION_LOCK:
        matching_handler: logging.FileHandler | None = None
        for handler in tuple(logger.handlers):
            if not _is_jaos_owned(handler):
                continue
            if (
                isinstance(handler, logging.FileHandler)
                and Path(handler.baseFilename) == log_file
                and matching_handler is None
            ):
                matching_handler = handler
                continue
            _close_jaos_handler(handler)

        logs_directory.mkdir(parents=True, exist_ok=True)

        if matching_handler is None:
            matching_handler = logging.FileHandler(
                log_file,
                encoding="utf-8",
                delay=True,
            )
            setattr(
                matching_handler,
                _OWNED_HANDLER_ATTRIBUTE,
                True,
            )
            matching_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
            logger.addHandler(matching_handler)

        matching_handler.setLevel(level)
        logger.setLevel(level)
        logger.propagate = False

    return log_file


def reset_runtime_logging() -> None:
    """Flush, detach, and close only JAOS-owned runtime handlers."""

    with _CONFIGURATION_LOCK:
        for handler in tuple(logger.handlers):
            if _is_jaos_owned(handler):
                _close_jaos_handler(handler)

        logger.setLevel(_INITIAL_LOGGER_LEVEL)
        logger.propagate = _INITIAL_LOGGER_PROPAGATE


__all__ = [
    "LOGGER_NAME",
    "SYSTEM_LOG_FILENAME",
    "configure_runtime_logging",
    "logger",
    "reset_runtime_logging",
]
