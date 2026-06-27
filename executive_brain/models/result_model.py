from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional
from executive_brain.common.enums import LifecycleStatus


@dataclass
class ResultModel:
    success: bool
    message: str
    related_execution_plan_id: Optional[str] = None
    status: LifecycleStatus = LifecycleStatus.COMPLETED

    result_id: str = field(
        default_factory=lambda: f"RES-{uuid4()}"
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    metadata: dict = field(
        default_factory=dict
    )

    def __post_init__(self):
        if not self.message.strip():
            raise ValueError("message cannot be empty.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def to_dict(self):
        return {
            "result_id": self.result_id,
            "success": self.success,
            "message": self.message,
            "related_execution_plan_id": self.related_execution_plan_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }