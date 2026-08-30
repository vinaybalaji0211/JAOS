import pytest

from executive_brain.brain.executive_brain import ExecutiveBrain


def test_complete_executive_pipeline():
    brain = ExecutiveBrain()
    brain.initialize()

    result = brain.execute("Create project folder")

    assert result.success is True

    summary = brain.get_system_summary()
    counts = summary["registry_counts"]

    assert counts["mission"] == 1
    assert counts["execution_plan"] == 1
    assert counts["decision"] == 1
    assert counts["result"] == 1


def test_executive_pipeline_updates_working_memory():
    brain = ExecutiveBrain()
    brain.initialize()

    result = brain.execute("Create project folder")

    memory = brain.get_memory_manager().get_memory()

    assert memory.current_user_request == "Create project folder"
    assert memory.current_mission_id == result.metadata["mission_id"]
    assert memory.current_execution_plan_id == result.related_execution_plan_id
    assert memory.current_decision_id == result.metadata["decision_id"]
    assert memory.current_result_id == result.result_id
    assert memory.active_context["last_result_success"] is True


def test_system_summary_includes_working_memory():
    brain = ExecutiveBrain()
    brain.initialize()

    result = brain.execute("Create project folder")

    summary = brain.get_system_summary()
    working_memory = summary["working_memory"]

    assert working_memory["current_user_request"] == "Create project folder"
    assert working_memory["current_result_id"] == result.result_id
    assert working_memory["active_context"]["last_result_success"] is True


def test_multiple_requests_update_counts_and_refresh_memory():
    brain = ExecutiveBrain()
    brain.initialize()

    first_result = brain.execute("Task One")
    second_result = brain.execute("Task Two")

    summary = brain.get_system_summary()
    counts = summary["registry_counts"]
    memory = brain.get_memory_manager().get_memory()

    assert counts["mission"] == 2
    assert counts["execution_plan"] == 2
    assert counts["decision"] == 2
    assert counts["result"] == 2

    assert memory.current_user_request == "Task Two"
    assert memory.current_result_id == second_result.result_id
    assert memory.current_result_id != first_result.result_id


def test_empty_request():
    brain = ExecutiveBrain()
    brain.initialize()

    with pytest.raises(ValueError):
        brain.execute("")