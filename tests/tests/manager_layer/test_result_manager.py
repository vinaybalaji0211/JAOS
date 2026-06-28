import pytest

from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.managers.result_manager import ResultManager
from executive_brain.models.result_model import ResultModel


def test_result_manager_initializes():
    manager = ResultManager(RegistryManager())
    assert manager.get_status() == "INITIALIZED"


def test_invalid_registry_manager():
    with pytest.raises(TypeError):
        ResultManager("invalid")


def test_initialize():
    manager = ResultManager(RegistryManager())

    assert manager.initialize() is True
    assert manager.get_status() == "READY"


def test_health_check():
    manager = ResultManager(RegistryManager())

    manager.initialize()

    assert manager.health_check() == {
        "result_manager": True,
        "registry_manager": True,
    }


def test_add_and_get_result():
    registry = RegistryManager()
    manager = ResultManager(registry)

    result = ResultModel(
        success=True,
        message="Completed successfully."
    )

    manager.add_result(result)

    assert manager.get_result(result.result_id) == result


def test_list_results():
    registry = RegistryManager()
    manager = ResultManager(registry)

    result = ResultModel(
        success=True,
        message="Completed."
    )

    manager.add_result(result)

    assert manager.list_results() == [result]


def test_successful_results():
    registry = RegistryManager()
    manager = ResultManager(registry)

    success = ResultModel(True, "OK")
    failure = ResultModel(False, "Failed")

    manager.add_result(success)
    manager.add_result(failure)

    assert manager.get_successful_results() == [success]


def test_failed_results():
    registry = RegistryManager()
    manager = ResultManager(registry)

    success = ResultModel(True, "OK")
    failure = ResultModel(False, "Failed")

    manager.add_result(success)
    manager.add_result(failure)

    assert manager.get_failed_results() == [failure]


def test_statistics():
    registry = RegistryManager()
    manager = ResultManager(registry)

    manager.add_result(ResultModel(True, "OK"))
    manager.add_result(ResultModel(True, "OK"))
    manager.add_result(ResultModel(False, "Failed"))

    assert manager.total_results() == 3
    assert manager.successful_result_count() == 2
    assert manager.failed_result_count() == 1
    assert manager.success_rate() == pytest.approx(66.666, rel=1e-2)