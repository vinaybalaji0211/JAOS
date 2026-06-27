from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class ContextSnapshotModel:
    """
    Represents what JAOS knew at the moment a decision was made.

    NOTE:
    ContextSnapshotModel does NOT control runtime state.
    It only captures a snapshot of state for explainability.
    """

    current_user: str = "UNKNOWN"

    active_project: str = "NONE"

    active_mode: str = "DESKTOP"

    active_ai_provider: str = "NONE"

    active_agent: str = "NONE"

    active_workflow: str = "NONE"

    internet_status: str = "UNKNOWN"

    system_status: str = "UNKNOWN"

    snapshot_id: str = field(
        default_factory=lambda: f"CTX-{uuid4()}"
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    metadata: dict = field(
        default_factory=dict
    )

    def add_metadata(self, key, value):

        self.metadata[key] = value

    def to_dict(self):

        return {
            "snapshot_id": self.snapshot_id,
            "current_user": self.current_user,
            "active_project": self.active_project,
            "active_mode": self.active_mode,
            "active_ai_provider": self.active_ai_provider,
            "active_agent": self.active_agent,
            "active_workflow": self.active_workflow,
            "internet_status": self.internet_status,
            "system_status": self.system_status,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }