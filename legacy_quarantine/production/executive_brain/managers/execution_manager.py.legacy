"""
JAOS Component: ExecutionManager

Purpose:
    Simulate execution of approved execution plans inside the Executive Brain.

Responsibilities:
    - Retrieve execution plans
    - Update execution plan status
    - Create ResultModel objects
    - Store results through RegistryManager
    - Report manager status and health

Non-Responsibilities:
    - Execute real OS actions
    - Call tools
    - Call AI models
    - Manage memory
"""

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.result_model import ResultModel


class ExecutionManager:
    """Manager responsible for simulated execution of execution plans."""

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
            "execution_manager": self.status == "READY",
            "registry_manager": self.registry_manager is not None,
        }

    def execute_plan(self, execution_plan_id: str):
        execution_plan = (
            self.registry_manager
            .execution_plan_registry
            .get_execution_plan(execution_plan_id)
        )

        if execution_plan is None:
            raise KeyError(f"Execution plan not found: {execution_plan_id}")

        execution_plan.update_status(LifecycleStatus.ACTIVE)
        self.registry_manager.execution_plan_registry.update_execution_plan(
            execution_plan
        )

        result = ResultModel(
            success=True,
            message=(
                "Execution completed successfully for "
                f"{execution_plan.target_platform}:"
                f"{execution_plan.target_service}"
            ),
            related_execution_plan_id=execution_plan.execution_plan_id,
            status=LifecycleStatus.COMPLETED,
        )

        result.add_metadata("execution_mode", "simulated")
        result.add_metadata(
            "target_platform",
            execution_plan.target_platform,
        )
        result.add_metadata(
            "target_service",
            execution_plan.target_service,
        )

        self.registry_manager.result_registry.add_result(result)

        execution_plan.update_status(LifecycleStatus.COMPLETED)
        self.registry_manager.execution_plan_registry.update_execution_plan(
            execution_plan
        )

        return result