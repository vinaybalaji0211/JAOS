import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.execution_manager import ExecutionManager
from executive_brain.managers.planning_manager import PlanningManager
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.result_model import ResultModel


def test_execution_manager_initializes():
    registry_manager = RegistryManager()
    execution_manager = ExecutionManager(registry_manager)

    assert execution_manager.get_status() == "INITIALIZED"


def test_execution_manager_rejects_invalid_registry_manager():
    with pytest.raises(TypeError):
        ExecutionManager("not a registry manager")


def test_execution_manager_initialize():
    registry_manager = RegistryManager()
    execution_manager = ExecutionManager(registry_manager)

    assert execution_manager.initialize() is True
    assert execution_manager.get_status() == "READY"


def test_execution_manager_health_check():
    registry_manager = RegistryManager()
    execution_manager = ExecutionManager(registry_manager)

    execution_manager.initialize()

    assert execution_manager.health_check() == {
        "execution_manager": True,
        "registry_manager": True,
    }


def test_execute_plan_creates_result():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)
    execution_manager = ExecutionManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
        related_mission_id="MIS-001",
    )

    result = execution_manager.execute_plan(
        execution_plan.execution_plan_id
    )

    assert isinstance(result, ResultModel)
    assert result.success is True
    assert result.related_execution_plan_id == execution_plan.execution_plan_id
    assert result.status == LifecycleStatus.COMPLETED


def test_execute_plan_stores_result():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)
    execution_manager = ExecutionManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
    )

    result = execution_manager.execute_plan(
        execution_plan.execution_plan_id
    )

    stored_result = registry_manager.result_registry.get_result(
        result.result_id
    )

    assert stored_result == result


def test_execute_plan_updates_plan_status_to_completed():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)
    execution_manager = ExecutionManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="filesystem",
    )

    execution_manager.execute_plan(execution_plan.execution_plan_id)

    stored_plan = (
        registry_manager
        .execution_plan_registry
        .get_execution_plan(execution_plan.execution_plan_id)
    )

    assert stored_plan.status == LifecycleStatus.COMPLETED


def test_execute_plan_adds_metadata_to_result():
    registry_manager = RegistryManager()
    planning_manager = PlanningManager(registry_manager)
    execution_manager = ExecutionManager(registry_manager)

    execution_plan = planning_manager.create_execution_plan(
        target_platform="windows",
        target_service="browser",
    )

    result = execution_manager.execute_plan(
        execution_plan.execution_plan_id
    )

    assert result.metadata["execution_mode"] == "simulated"
    assert result.metadata["target_platform"] == "windows"
    assert result.metadata["target_service"] == "browser"


def test_execute_missing_plan_raises_key_error():
    registry_manager = RegistryManager()
    execution_manager = ExecutionManager(registry_manager)

    with pytest.raises(KeyError):
        execution_manager.execute_plan("PLAN-DOES-NOT-EXIST")