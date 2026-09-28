"""
JAOS Component: PlanningManager

Purpose:
    Create and manage simple execution plans for JAOS missions.

Responsibilities:
    - Create execution plans
    - Store execution plans through RegistryManager
    - Report planning status
    - Provide planning health information

Non-Responsibilities:
    - Execute plans
    - Make decisions
    - Call AI models
    - Manage memory
"""

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.execution_plan_model import ExecutionPlanModel


class PlanningManager:
    """Manager responsible for creating and registering execution plans."""

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
            "planning_manager": self.status == "READY",
            "registry_manager": self.registry_manager is not None,
        }

    def create_execution_plan(
        self,
        target_platform: str,
        target_service: str,
        related_mission_id: str | None = None,
        metadata: dict | None = None,
    ):
        execution_plan = ExecutionPlanModel(
            target_platform=target_platform,
            target_service=target_service,
            related_mission_id=related_mission_id,
            status=LifecycleStatus.CREATED,
        )

        if metadata:
            for key, value in metadata.items():
                execution_plan.add_metadata(key, value)

        self.registry_manager.execution_plan_registry.add_execution_plan(
            execution_plan
        )

        return execution_plan

    def list_execution_plans(self):
        return (
            self.registry_manager
            .execution_plan_registry
            .list_execution_plans()
        )

    def get_execution_plan(self, execution_plan_id: str):
        return (
            self.registry_manager
            .execution_plan_registry
            .get_execution_plan(execution_plan_id)
        )