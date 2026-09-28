from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from executive_brain.common.enums import LifecycleStatus, Priority


@dataclass
class IntentModel:
    intent_type: str
    source: str = "USER"
    priority: Priority = Priority.NORMAL
    confidence: float = 1.0
    status: LifecycleStatus = LifecycleStatus.ACTIVE
    intent_id: str = field(default_factory=lambda: f"INT-{uuid4()}")
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.intent_type.strip():
            raise ValueError("intent_type cannot be empty.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def to_dict(self):
        return {
            "intent_id": self.intent_id,
            "intent_type": self.intent_type,
            "source": self.source,
            "priority": self.priority.value,
            "confidence": self.confidence,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }