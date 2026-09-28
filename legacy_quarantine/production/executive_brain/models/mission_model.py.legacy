from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from executive_brain.common.enums import LifecycleStatus


@dataclass
class MissionModel:
    mission_name: str
    status: LifecycleStatus = LifecycleStatus.CREATED
    progress: float = 0.0
    current_step: int = 0
    total_steps: int = 0
    related_goal_id: str | None = None
    steps: list = field(default_factory=list)
    mission_id: str = field(default_factory=lambda: f"MIS-{uuid4()}")
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.mission_name.strip():
            raise ValueError("mission_name cannot be empty.")

        if not 0.0 <= self.progress <= 100.0:
            raise ValueError("progress must be between 0 and 100.")

        if self.total_steps < 0:
            raise ValueError("total_steps cannot be negative.")

        if self.current_step < 0:
            raise ValueError("current_step cannot be negative.")

        if self.current_step > self.total_steps:
            raise ValueError("current_step cannot exceed total_steps.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def update_progress(self, progress):
        if not 0.0 <= progress <= 100.0:
            raise ValueError("progress must be between 0 and 100.")
        self.progress = progress

    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "mission_name": self.mission_name,
            "status": self.status.value,
            "progress": self.progress,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "related_goal_id": self.related_goal_id,
            "steps": self.steps,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }