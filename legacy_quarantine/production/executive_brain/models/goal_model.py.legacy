from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from executive_brain.common.enums import LifecycleStatus, Priority


@dataclass
class GoalModel:
    goal_name: str
    priority: Priority = Priority.NORMAL
    status: LifecycleStatus = LifecycleStatus.CREATED
    related_decision_id: str | None = None
    success_criteria: str = ""
    goal_id: str = field(default_factory=lambda: f"GOAL-{uuid4()}")
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.goal_name.strip():
            raise ValueError("goal_name cannot be empty.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "goal_name": self.goal_name,
            "priority": self.priority.value,
            "status": self.status.value,
            "related_decision_id": self.related_decision_id,
            "success_criteria": self.success_criteria,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }