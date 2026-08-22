"""Canonical runtime lifecycle state contract for jaos_platform."""

from __future__ import annotations

from enum import Enum


class RuntimeLifecycleState(str, Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    INITIALIZED = "INITIALIZED"
    STARTING = "STARTING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    ROLLING_BACK = "ROLLING_BACK"
    FAILED = "FAILED"
