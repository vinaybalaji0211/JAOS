import pytest

from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.result_model import ResultModel
from executive_brain.registries.decision_registry import DecisionRegistry
from executive_brain.registries.execution_plan_registry import ExecutionPlanRegistry
from executive_brain.registries.goal_registry import GoalRegistry
from executive_brain.registries.intent_registry import IntentRegistry
from executive_brain.registries.mission_registry import MissionRegistry
from executive_brain.registries.result_registry import ResultRegistry


def test_registry_manager_initializes_all_registries():
    manager = RegistryManager()

    assert isinstance(manager.intent_registry, IntentRegistry)
    assert isinstance(manager.decision_registry, DecisionRegistry)
    assert isinstance(manager.goal_registry, GoalRegistry)
    assert isinstance(manager.mission_registry, MissionRegistry)
    assert isinstance(manager.execution_plan_registry, ExecutionPlanRegistry)
    assert isinstance(manager.result_registry, ResultRegistry)


def test_list_registries():
    manager = RegistryManager()

    assert manager.list_registries() == [
        "intent",
        "decision",
        "goal",
        "mission",
        "execution_plan",
        "result",
    ]


def test_get_registry_returns_correct_registry():
    manager = RegistryManager()

    assert manager.get_registry("intent") is manager.intent_registry
    assert manager.get_registry("decision") is manager.decision_registry
    assert manager.get_registry("goal") is manager.goal_registry
    assert manager.get_registry("mission") is manager.mission_registry
    assert manager.get_registry("execution_plan") is manager.execution_plan_registry
    assert manager.get_registry("result") is manager.result_registry


def test_get_registry_rejects_unknown_registry():
    manager = RegistryManager()

    with pytest.raises(KeyError):
        manager.get_registry("unknown")


def test_health_check_returns_true_for_all_registries():
    manager = RegistryManager()

    assert manager.health_check() == {
        "intent": True,
        "decision": True,
        "goal": True,
        "mission": True,
        "execution_plan": True,
        "result": True,
    }


def test_registry_counts_start_at_zero():
    manager = RegistryManager()

    assert manager.registry_counts() == {
        "intent": 0,
        "decision": 0,
        "goal": 0,
        "mission": 0,
        "execution_plan": 0,
        "result": 0,
    }


def test_registry_counts_update_after_adding_result():
    manager = RegistryManager()

    result = ResultModel(
        success=True,
        message="Execution completed",
    )

    manager.result_registry.add_result(result)

    assert manager.registry_counts()["result"] == 1