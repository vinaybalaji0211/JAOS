import pytest

from executive_brain.managers.planning_manager import PlanningManager
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.execution_plan_model import ExecutionPlanModel


def test_planning_manager_initializes():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    assert planning_manager.get_status() == "INITIALIZED"


def test_planning_manager_rejects_invalid_registry_manager():
    with pytest.raises(TypeError):
        PlanningManager("not a registry manager")


def test_planning_manager_initialize():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    assert planning_manager.initialize() is True
    assert planning_manager.get_status() == "READY"


def test_planning_manager_health_check():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    planning_manager.initialize()

    assert planning_manager.health_check() == {
        "planning_manager": True,
        "registry_manager": True,
    }


def test_create_execution_plan():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
        related_mission_id="MIS-001",
    )

    assert isinstance(execution_plan, ExecutionPlanModel)
    assert execution_plan.target_platform == "windows"
    assert execution_plan.target_service == "filesystem"
    assert execution_plan.related_mission_id == "MIS-001"

    stored_plan = (
        registry_manager
        .execution_plan_registry
        .get_execution_plan(execution_plan.execution_plan_id)
    )

    assert stored_plan == execution_plan


def test_create_execution_plan_with_metadata():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="browser",
        metadata={
            "priority": "high",
            "source": "test",
        },
    )

    assert execution_plan.metadata["priority"] == "high"
    assert execution_plan.metadata["source"] == "test"


def test_list_execution_plans():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
    )

    assert planning_manager.list_execution_plans() == [plan]


def test_get_execution_plan():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)

    plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
    )

    assert planning_manager.get_execution_plan(
        plan.execution_plan_id
    ) == plan