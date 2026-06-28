"""
JAOS Component: DecisionManager

Purpose:
    Create and manage decisions inside the Executive Brain.

Responsibilities:
    - Create DecisionModel objects
    - Store decisions through RegistryManager
    - Retrieve decisions
    - Report manager status and health

Non-Responsibilities:
    - Execute plans
    - Call AI models
    - Manage memory
    - Perform tool execution
"""

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.decision_model import DecisionModel


class DecisionManager:
    """Manager responsible for creating and registering decisions."""

    def __init__(self, registry_manager: RegistryManager):
        if not isinstance(registry_manager, RegistryManager):
            raise TypeError(
                "registry_manager must be an instance of RegistryManager."
            )

        self.registry_manager = registry_manager
        self.status = "INITIALIZED"

    def initialize(self):
        self.status = "READY"
        return True

    def get_status(self):
        return self.status

    def health_check(self):
        return {
            "decision_manager": self.status == "READY",
            "registry_manager": self.registry_manager is not None,
        }

    def create_decision(
        self,
        decision_type: str,
        reason: str,
        confidence: float = 1.0,
        related_intent_id: str | None = None,
        related_context_snapshot_id: str | None = None,
        metadata: dict | None = None,
    ):
        decision = DecisionModel(
            decision_type=decision_type,
            reason=reason,
            confidence=confidence,
            status=LifecycleStatus.CREATED,
            related_intent_id=related_intent_id,
            related_context_snapshot_id=related_context_snapshot_id,
        )

        if metadata:
            for key, value in metadata.items():
                decision.add_metadata(key, value)

        self.registry_manager.decision_registry.add(
            decision.decision_id,
            decision,
        )

        return decision

    def get_decision(self, decision_id: str):
        return self.registry_manager.decision_registry.get(decision_id)

    def list_decisions(self):
        return self.registry_manager.decision_registry.list_all()

    def get_decisions_by_type(self, decision_type: str):
        return self.registry_manager.decision_registry.get_by_type(
            decision_type
        )

    def get_decisions_by_status(self, status: LifecycleStatus):
        return self.registry_manager.decision_registry.get_by_status(status)