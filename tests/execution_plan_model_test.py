from executive_brain.models.execution_plan_model import ExecutionPlanModel
from executive_brain.common.enums import LifecycleStatus

plan = ExecutionPlanModel(
    target_platform="PC_CONTROL",
    target_service="ApplicationLauncher",
    related_mission_id="MIS-001"
)

plan.update_status(LifecycleStatus.ACTIVE)

plan.add_metadata(
    "application",
    "VS Code"
)

print()
print(plan.to_dict())