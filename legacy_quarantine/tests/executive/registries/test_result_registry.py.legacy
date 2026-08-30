import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.result_model import ResultModel
from executive_brain.registries.result_registry import ResultRegistry


def test_add_and_get_result():
    registry = ResultRegistry()
    result = ResultModel(success=True, message="Execution completed")

    registry.add_result(result)

    assert registry.get_result(result.result_id) == result
    assert registry.count() == 1


def test_reject_non_result_model():
    registry = ResultRegistry()

    with pytest.raises(TypeError):
        registry.add_result("not a result")


def test_reject_duplicate_result():
    registry = ResultRegistry()
    result = ResultModel(success=True, message="Execution completed")

    registry.add_result(result)

    with pytest.raises(ValueError):
        registry.add_result(result)


def test_update_result():
    registry = ResultRegistry()
    result = ResultModel(success=True, message="Execution completed")

    registry.add_result(result)

    result.update_status(LifecycleStatus.ACTIVE)
    registry.update_result(result)

    updated = registry.get_result(result.result_id)

    assert updated.status == LifecycleStatus.ACTIVE


def test_remove_result():
    registry = ResultRegistry()
    result = ResultModel(success=True, message="Execution completed")

    registry.add_result(result)
    removed = registry.remove_result(result.result_id)

    assert removed == result
    assert registry.get_result(result.result_id) is None
    assert registry.count() == 0


def test_list_results():
    registry = ResultRegistry()

    result_1 = ResultModel(success=True, message="Execution completed")
    result_2 = ResultModel(success=False, message="Execution failed")

    registry.add_result(result_1)
    registry.add_result(result_2)

    assert registry.list_results() == [result_1, result_2]


def test_get_by_status():
    registry = ResultRegistry()

    completed_result = ResultModel(
        success=True,
        message="Execution completed",
        status=LifecycleStatus.COMPLETED,
    )

    active_result = ResultModel(
        success=False,
        message="Execution still active",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_result(completed_result)
    registry.add_result(active_result)

    assert registry.get_by_status(LifecycleStatus.COMPLETED) == [
        completed_result
    ]


def test_get_by_execution_plan():
    registry = ResultRegistry()

    result_1 = ResultModel(
        success=True,
        message="Execution completed",
        related_execution_plan_id="PLAN-001",
    )

    result_2 = ResultModel(
        success=False,
        message="Execution failed",
        related_execution_plan_id="PLAN-002",
    )

    registry.add_result(result_1)
    registry.add_result(result_2)

    assert registry.get_by_execution_plan("PLAN-001") == [result_1]


def test_get_successful_results():
    registry = ResultRegistry()

    success_result = ResultModel(
        success=True,
        message="Execution completed",
    )

    failed_result = ResultModel(
        success=False,
        message="Execution failed",
    )

    registry.add_result(success_result)
    registry.add_result(failed_result)

    assert registry.get_successful_results() == [success_result]


def test_get_failed_results():
    registry = ResultRegistry()

    success_result = ResultModel(
        success=True,
        message="Execution completed",
    )

    failed_result = ResultModel(
        success=False,
        message="Execution failed",
    )

    registry.add_result(success_result)
    registry.add_result(failed_result)

    assert registry.get_failed_results() == [failed_result]


def test_get_completed_results():
    registry = ResultRegistry()

    completed_result = ResultModel(
        success=True,
        message="Execution completed",
        status=LifecycleStatus.COMPLETED,
    )

    active_result = ResultModel(
        success=False,
        message="Execution active",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_result(completed_result)
    registry.add_result(active_result)

    assert registry.get_completed_results() == [completed_result]


def test_get_incomplete_results():
    registry = ResultRegistry()

    completed_result = ResultModel(
        success=True,
        message="Execution completed",
        status=LifecycleStatus.COMPLETED,
    )

    active_result = ResultModel(
        success=False,
        message="Execution active",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_result(completed_result)
    registry.add_result(active_result)

    assert registry.get_incomplete_results() == [active_result]