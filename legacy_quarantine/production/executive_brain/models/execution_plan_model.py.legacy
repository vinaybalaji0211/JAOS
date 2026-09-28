from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from executive_brain.common.enums import LifecycleStatus


@dataclass
class ExecutionPlanModel:
    target_platform: str
    target_service: str
    status: LifecycleStatus = LifecycleStatus.CREATED
    related_mission_id: str | None = None

    execution_plan_id: str = field(
        default_factory=lambda: f"PLAN-{uuid4()}"
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    metadata: dict = field(
        default_factory=dict
    )

    def __post_init__(self):
        if not self.target_platform.strip():
            raise ValueError("target_platform cannot be empty.")

        if not self.target_service.strip():
            raise ValueError("target_service cannot be empty.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def to_dict(self):
        return {
            "execution_plan_id": self.execution_plan_id,
            "target_platform": self.target_platform,
            "target_service": self.target_service,
            "status": self.status.value,
            "related_mission_id": self.related_mission_id,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }