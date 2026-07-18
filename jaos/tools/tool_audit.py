from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class ToolAuditRecord:
    tool_name: str
    success: bool
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.tool_name.strip():
            raise ValueError("Tool audit record tool name cannot be empty")


class ToolAuditLogger:
    """
    In-memory audit logger for Tool Platform Alpha.

    Persistent audit storage will be added later through the Security Platform.
    """

    def __init__(self) -> None:
        self._records: list[ToolAuditRecord] = []

    def record(self, record: ToolAuditRecord) -> None:
        self._records.append(record)

    def list_records(self) -> tuple[ToolAuditRecord, ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()