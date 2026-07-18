from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class AIProviderLifecycleState(str, Enum):
    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"
    FAILED = "failed"


@dataclass
class AIProviderState:
    """
    Runtime state for an AI provider.

    This stores live provider status and metrics.
    It must not store secrets or static configuration.
    """

    name: str
    lifecycle: AIProviderLifecycleState = AIProviderLifecycleState.CREATED
    enabled: bool = True
    available: bool = False
    healthy: bool = False
    current_model: str | None = None
    request_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_seconds: float = 0.0
    last_latency_seconds: float | None = None
    last_error: str | None = None
    last_health_check_at: datetime | None = None
    last_initialized_at: datetime | None = None
    last_shutdown_at: datetime | None = None
    restart_count: int = 0

    def __post_init__(self) -> None:
        normalized_name = self.name.strip().lower()

        if not normalized_name:
            raise ValueError("Provider state name cannot be empty")

        self.name = normalized_name

    @property
    def average_latency_seconds(self) -> float:
        if self.success_count == 0:
            return 0.0

        return self.total_latency_seconds / self.success_count

    def mark_initializing(self) -> None:
        self.lifecycle = AIProviderLifecycleState.INITIALIZING
        self.available = False
        self.healthy = False

    def mark_initialized(self, *, model: str | None = None) -> None:
        self.lifecycle = AIProviderLifecycleState.INITIALIZED
        self.available = True
        self.healthy = True
        self.last_error = None
        self.last_initialized_at = self._now()

        if model is not None:
            stripped_model = model.strip()
            self.current_model = stripped_model if stripped_model else None

    def mark_shutting_down(self) -> None:
        self.lifecycle = AIProviderLifecycleState.SHUTTING_DOWN
        self.available = False
        self.healthy = False

    def mark_shutdown(self) -> None:
        self.lifecycle = AIProviderLifecycleState.SHUTDOWN
        self.available = False
        self.healthy = False
        self.last_shutdown_at = self._now()

    def mark_failed(self, error: Exception | str) -> None:
        self.lifecycle = AIProviderLifecycleState.FAILED
        self.available = False
        self.healthy = False
        self.last_error = str(error)

    def mark_health_check(self, *, healthy: bool, error: Exception | str | None = None) -> None:
        self.last_health_check_at = self._now()
        self.healthy = healthy
        self.available = healthy and self.enabled

        if healthy:
            self.last_error = None
        elif error is not None:
            self.last_error = str(error)

    def disable(self) -> None:
        self.enabled = False
        self.available = False

    def enable(self) -> None:
        self.enabled = True
        self.available = self.healthy

    def record_success(self, *, latency_seconds: float = 0.0) -> None:
        if latency_seconds < 0:
            raise ValueError("Latency cannot be negative")

        self.request_count += 1
        self.success_count += 1
        self.last_latency_seconds = latency_seconds
        self.total_latency_seconds += latency_seconds
        self.last_error = None

    def record_failure(self, error: Exception | str) -> None:
        self.request_count += 1
        self.failure_count += 1
        self.last_error = str(error)

    def record_restart(self) -> None:
        self.restart_count += 1

    def reset_metrics(self) -> None:
        self.request_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_latency_seconds = 0.0
        self.last_latency_seconds = None

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)