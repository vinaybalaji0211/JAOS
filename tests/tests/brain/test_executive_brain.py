import pytest

from executive_brain.brain.executive_brain import ExecutiveBrain
from executive_brain.models.result_model import ResultModel


def test_initialization():
    brain = ExecutiveBrain()

    assert brain.get_status() == "INITIALIZED"


def test_initialize():
    brain = ExecutiveBrain()

    assert brain.initialize() is True
    assert brain.get_status() == "READY"


def test_registry_manager_exists():
    brain = ExecutiveBrain()

    assert brain.get_registry_manager() is not None


def test_system_summary():
    brain = ExecutiveBrain()

    summary = brain.get_system_summary()

    assert summary["registry_manager"] is True
    assert isinstance(summary["registries"], list)
    assert isinstance(summary["registry_counts"], dict)
    assert "managers" in summary


def test_health_check():
    brain = ExecutiveBrain()

    brain.initialize()

    health = brain.health_check()

    assert health["executive_brain"] is True
    assert health["registry_manager"]["intent"] is True
    assert health["planning_manager"]["planning_manager"] is True
    assert health["decision_manager"]["decision_manager"] is True
    assert health["mission_manager"]["mission_manager"] is True
    assert health["execution_manager"]["execution_manager"] is True
    assert health["result_manager"]["result_manager"] is True


def test_execute_returns_result():
    brain = ExecutiveBrain()
    brain.initialize()

    result = brain.execute("Create project folder")

    assert isinstance(result, ResultModel)
    assert result.success is True
    assert result.metadata["user_request"] == "Create project folder"
    assert "mission_id" in result.metadata
    assert "decision_id" in result.metadata


def test_execute_rejects_empty_request():
    brain = ExecutiveBrain()
    brain.initialize()

    with pytest.raises(ValueError):
        brain.execute("")