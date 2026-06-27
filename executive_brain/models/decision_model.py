from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional
from executive_brain.common.enums import LifecycleStatus


@dataclass
class DecisionModel:
    decision_type: str
    reason: str
    confidence: float = 1.0
    status: LifecycleStatus = LifecycleStatus.CREATED
    related_intent_id: Optional[str] = None
    related_context_snapshot_id: Optional[str] = None

    decision_id: str = field(
        default_factory=lambda: f"DEC-{uuid4()}"
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )

    metadata: dict = field(
        default_factory=dict
    )

    def __post_init__(self):
        if not self.decision_type.strip():
            raise ValueError("decision_type cannot be empty.")

        if not self.reason.strip():
            raise ValueError("reason cannot be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def update_status(self, status: LifecycleStatus):
        self.status = status

    def to_dict(self):
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type,
            "reason": self.reason,
            "confidence": self.confidence,
            "status": self.status.value,
            "related_intent_id": self.related_intent_id,
            "related_context_snapshot_id": self.related_context_snapshot_id,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }