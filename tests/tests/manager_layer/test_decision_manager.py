import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.decision_manager import DecisionManager
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.decision_model import DecisionModel


def test_decision_manager_initializes():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    assert decision_manager.get_status() == "INITIALIZED"


def test_decision_manager_rejects_invalid_registry_manager():
    with pytest.raises(TypeError):
        DecisionManager("not a registry manager")


def test_decision_manager_initialize():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    assert decision_manager.initialize() is True
    assert decision_manager.get_status() == "READY"


def test_decision_manager_health_check():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision_manager.initialize()

    assert decision_manager.health_check() == {
        "decision_manager": True,
        "registry_manager": True,
    }


def test_create_decision():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="safe_execution",
        reason="Operation requires safe execution policy.",
        confidence=0.9,
        related_intent_id="INT-001",
    )

    assert isinstance(decision, DecisionModel)
    assert decision.decision_type == "safe_execution"
    assert decision.reason == "Operation requires safe execution policy."
    assert decision.confidence == 0.9
    assert decision.related_intent_id == "INT-001"

    stored_decision = registry_manager.decision_registry.get(
        decision.decision_id
    )

    assert stored_decision == decision


def test_create_decision_with_metadata():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="permission_required",
        reason="Destructive operation requires permission.",
        metadata={
            "risk_level": "high",
            "requires_user_approval": True,
        },
    )

    assert decision.metadata["risk_level"] == "high"
    assert decision.metadata["requires_user_approval"] is True


def test_get_decision():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="continue",
        reason="Plan is safe to continue.",
    )

    assert decision_manager.get_decision(decision.decision_id) == decision


def test_list_decisions():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="continue",
        reason="Plan is safe to continue.",
    )

    assert decision_manager.list_decisions() == [decision]


def test_get_decisions_by_type():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="continue",
        reason="Plan is safe to continue.",
    )

    decision_manager.create_decision(
        decision_type="stop",
        reason="Plan is unsafe.",
    )

    assert decision_manager.get_decisions_by_type("continue") == [decision]


def test_get_decisions_by_status():
    registry_manager = RegistryManager()
    decision_manager = DecisionManager(registry_manager)

    decision = decision_manager.create_decision(
        decision_type="continue",
        reason="Plan is safe to continue.",
    )

    assert decision_manager.get_decisions_by_status(
        LifecycleStatus.CREATED
    ) == [decision]