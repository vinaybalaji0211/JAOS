import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.execution_plan_model import ExecutionPlanModel
from executive_brain.registries.execution_plan_registry import ExecutionPlanRegistry


def test_add_and_get_execution_plan():
    registry = ExecutionPlanRegistry()

    execution_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    registry.add_execution_plan(execution_plan)

    assert registry.get_execution_plan(
        execution_plan.execution_plan_id
    ) == execution_plan

    assert registry.count() == 1


def test_reject_non_execution_plan_model():
    registry = ExecutionPlanRegistry()

    with pytest.raises(TypeError):
        registry.add_execution_plan("not an execution plan")


def test_reject_duplicate_execution_plan():
    registry = ExecutionPlanRegistry()

    execution_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    registry.add_execution_plan(execution_plan)

    with pytest.raises(ValueError):
        registry.add_execution_plan(execution_plan)


def test_update_execution_plan():
    registry = ExecutionPlanRegistry()

    execution_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    registry.add_execution_plan(execution_plan)

    execution_plan.update_status(LifecycleStatus.ACTIVE)

    registry.update_execution_plan(execution_plan)

    updated = registry.get_execution_plan(
        execution_plan.execution_plan_id
    )

    assert updated.status == LifecycleStatus.ACTIVE


def test_remove_execution_plan():
    registry = ExecutionPlanRegistry()

    execution_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    registry.add_execution_plan(execution_plan)

    removed = registry.remove_execution_plan(
        execution_plan.execution_plan_id
    )

    assert removed == execution_plan

    assert registry.get_execution_plan(
        execution_plan.execution_plan_id
    ) is None

    assert registry.count() == 0


def test_list_execution_plans():
    registry = ExecutionPlanRegistry()

    execution_plan_1 = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    execution_plan_2 = ExecutionPlanModel(
        target_platform="android",
        target_service="notifications",
    )

    registry.add_execution_plan(execution_plan_1)
    registry.add_execution_plan(execution_plan_2)

    assert registry.list_execution_plans() == [
        execution_plan_1,
        execution_plan_2,
    ]


def test_get_by_status():
    registry = ExecutionPlanRegistry()

    active_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
        status=LifecycleStatus.ACTIVE,
    )

    completed_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="browser",
        status=LifecycleStatus.COMPLETED,
    )

    registry.add_execution_plan(active_plan)
    registry.add_execution_plan(completed_plan)

    assert registry.get_by_status(
        LifecycleStatus.ACTIVE
    ) == [active_plan]


def test_get_by_mission():
    registry = ExecutionPlanRegistry()

    execution_plan_1 = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
        related_mission_id="MIS-001",
    )

    execution_plan_2 = ExecutionPlanModel(
        target_platform="android",
        target_service="notifications",
        related_mission_id="MIS-002",
    )

    registry.add_execution_plan(execution_plan_1)
    registry.add_execution_plan(execution_plan_2)

    assert registry.get_by_mission("MIS-001") == [
        execution_plan_1
    ]


def test_get_by_target_platform():
    registry = ExecutionPlanRegistry()

    windows_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    android_plan = ExecutionPlanModel(
        target_platform="android",
        target_service="notifications",
    )

    registry.add_execution_plan(windows_plan)
    registry.add_execution_plan(android_plan)

    assert registry.get_by_target_platform("windows") == [
        windows_plan
    ]


def test_get_by_target_service():
    registry = ExecutionPlanRegistry()

    filesystem_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
    )

    browser_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="browser",
    )

    registry.add_execution_plan(filesystem_plan)
    registry.add_execution_plan(browser_plan)

    assert registry.get_by_target_service("filesystem") == [
        filesystem_plan
    ]


def test_get_active_execution_plans():
    registry = ExecutionPlanRegistry()

    active_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
        status=LifecycleStatus.ACTIVE,
    )

    pending_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="browser",
        status=LifecycleStatus.PENDING,
    )

    registry.add_execution_plan(active_plan)
    registry.add_execution_plan(pending_plan)

    assert registry.get_active_execution_plans() == [
        active_plan
    ]


def test_get_completed_execution_plans():
    registry = ExecutionPlanRegistry()

    completed_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
        status=LifecycleStatus.COMPLETED,
    )

    active_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="browser",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_execution_plan(completed_plan)
    registry.add_execution_plan(active_plan)

    assert registry.get_completed_execution_plans() == [
        completed_plan
    ]


def test_get_incomplete_execution_plans():
    registry = ExecutionPlanRegistry()

    completed_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="filesystem",
        status=LifecycleStatus.COMPLETED,
    )

    active_plan = ExecutionPlanModel(
        target_platform="windows",
        target_service="browser",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_execution_plan(completed_plan)
    registry.add_execution_plan(active_plan)

    assert registry.get_incomplete_execution_plans() == [
        active_plan
    ]