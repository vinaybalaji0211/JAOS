import pytest

from executive_brain.memory.working_memory import WorkingMemory


def test_initial_state():
    memory = WorkingMemory()

    assert memory.current_user_request is None
    assert memory.active_context == {}


def test_set_user_request():
    memory = WorkingMemory()

    memory.set_user_request("Open Chrome")

    assert memory.current_user_request == "Open Chrome"


def test_empty_request():
    memory = WorkingMemory()

    with pytest.raises(ValueError):
        memory.set_user_request("")


def test_set_mission():
    memory = WorkingMemory()

    memory.set_mission("MIS-001")

    assert memory.current_mission_id == "MIS-001"


def test_set_execution_plan():
    memory = WorkingMemory()

    memory.set_execution_plan("PLAN-001")

    assert memory.current_execution_plan_id == "PLAN-001"


def test_set_decision():
    memory = WorkingMemory()

    memory.set_decision("DEC-001")

    assert memory.current_decision_id == "DEC-001"


def test_set_result():
    memory = WorkingMemory()

    memory.set_result("RES-001")

    assert memory.current_result_id == "RES-001"


def test_add_context():
    memory = WorkingMemory()

    memory.add_context("language", "python")

    assert memory.active_context["language"] == "python"


def test_clear():
    memory = WorkingMemory()

    memory.set_user_request("Test")
    memory.set_mission("MIS-001")
    memory.add_context("a", 1)

    memory.clear()

    assert memory.current_user_request is None
    assert memory.current_mission_id is None
    assert memory.active_context == {}


def test_to_dict():
    memory = WorkingMemory()

    memory.set_user_request("Build JAOS")

    data = memory.to_dict()

    assert data["current_user_request"] == "Build JAOS"
    assert "updated_at" in data