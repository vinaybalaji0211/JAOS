from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ResponseFinishReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ResponseMetadata:
    provider: str
    model: str | None = None
    latency_seconds: float | None = None
    token_count: int | None = None
    finish_reason: ResponseFinishReason = ResponseFinishReason.UNKNOWN
    source_metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        provider = self.provider.strip().lower()

        if not provider:
            raise ValueError("Response metadata provider cannot be empty")

        object.__setattr__(self, "provider", provider)

        if self.model is not None:
            model = self.model.strip()
            object.__setattr__(self, "model", model or None)

        if self.latency_seconds is not None and self.latency_seconds < 0:
            raise ValueError("Response latency cannot be negative")

        if self.token_count is not None and self.token_count < 0:
            raise ValueError("Response token count cannot be negative")

        object.__setattr__(
            self,
            "finish_reason",
            self._normalize_finish_reason(self.finish_reason),
        )
        object.__setattr__(self, "source_metadata", dict(self.source_metadata or {}))

    @staticmethod
    def _normalize_finish_reason(
        finish_reason: ResponseFinishReason | str,
    ) -> ResponseFinishReason:
        if isinstance(finish_reason, ResponseFinishReason):
            return finish_reason

        try:
            return ResponseFinishReason(finish_reason.strip().lower())
        except ValueError:
            return ResponseFinishReason.UNKNOWN


@dataclass(frozen=True)
class ParsedResponse:
    text: str
    metadata: ResponseMetadata

    def __post_init__(self) -> None:
        text = self.text.strip()

        if not text:
            raise ValueError("Response text cannot be empty")

        object.__setattr__(self, "text", text)

    def is_complete(self) -> bool:
        return self.metadata.finish_reason in {
            ResponseFinishReason.STOP,
            ResponseFinishReason.UNKNOWN,
        }

    def is_truncated(self) -> bool:
        return self.metadata.finish_reason == ResponseFinishReason.LENGTH

    def is_error(self) -> bool:
        return self.metadata.finish_reason == ResponseFinishReason.ERROR