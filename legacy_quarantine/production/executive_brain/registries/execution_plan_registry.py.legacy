from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.execution_plan_model import ExecutionPlanModel
from executive_brain.registries.base_registry import BaseRegistry


class ExecutionPlanRegistry(BaseRegistry):
    """
    Registry responsible for storing and managing ExecutionPlanModel objects.

    Responsibilities:
    - Store execution plans
    - Retrieve execution plans
    - Update execution plans
    - Remove execution plans
    - Filter execution plans

    Non-Responsibilities:
    - Execute plans
    - Create plans
    - Decide plans
    - Schedule plans
    - Coordinate agents
    - Run tools
    """

    def __init__(self):
        super().__init__()

    def add_execution_plan(self, execution_plan: ExecutionPlanModel):
        if not isinstance(execution_plan, ExecutionPlanModel):
            raise TypeError(
                "execution_plan must be an instance of ExecutionPlanModel."
            )

        self.add(
            execution_plan.execution_plan_id,
            execution_plan
        )

    def get_execution_plan(self, execution_plan_id: str):
        return self.get(execution_plan_id)

    def update_execution_plan(self, execution_plan: ExecutionPlanModel):
        if not isinstance(execution_plan, ExecutionPlanModel):
            raise TypeError(
                "execution_plan must be an instance of ExecutionPlanModel."
            )

        self.update(
            execution_plan.execution_plan_id,
            execution_plan
        )

    def remove_execution_plan(self, execution_plan_id: str):
        return self.remove(execution_plan_id)

    def list_execution_plans(self):
        return self.list_all()

    def get_by_status(self, status: LifecycleStatus):
        return [
            execution_plan
            for execution_plan in self.list_all()
            if execution_plan.status == status
        ]

    def get_by_mission(self, mission_id: str):
        return [
            execution_plan
            for execution_plan in self.list_all()
            if execution_plan.related_mission_id == mission_id
        ]

    def get_by_target_platform(self, target_platform: str):
        return [
            execution_plan
            for execution_plan in self.list_all()
            if execution_plan.target_platform == target_platform
        ]

    def get_by_target_service(self, target_service: str):
        return [
            execution_plan
            for execution_plan in self.list_all()
            if execution_plan.target_service == target_service
        ]

    def get_active_execution_plans(self):
        return self.get_by_status(
            LifecycleStatus.ACTIVE
        )

    def get_completed_execution_plans(self):
        return self.get_by_status(
            LifecycleStatus.COMPLETED
        )

    def get_incomplete_execution_plans(self):
        return [
            execution_plan
            for execution_plan in self.list_all()
            if execution_plan.status != LifecycleStatus.COMPLETED
        ]