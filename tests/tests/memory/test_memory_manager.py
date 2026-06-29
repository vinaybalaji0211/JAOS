from executive_brain.memory.memory_manager import MemoryManager


def test_initialize():
    manager = MemoryManager()

    assert manager.get_status() == "READY"


def test_set_user_request():
    manager = MemoryManager()

    manager.set_user_request("Open Chrome")

    assert (
        manager.get_memory().current_user_request
        == "Open Chrome"
    )


def test_set_mission():
    manager = MemoryManager()

    manager.set_mission("MIS-001")

    assert (
        manager.get_memory().current_mission_id
        == "MIS-001"
    )


def test_set_execution_plan():
    manager = MemoryManager()

    manager.set_execution_plan("PLAN-001")

    assert (
        manager.get_memory().current_execution_plan_id
        == "PLAN-001"
    )


def test_set_decision():
    manager = MemoryManager()

    manager.set_decision("DEC-001")

    assert (
        manager.get_memory().current_decision_id
        == "DEC-001"
    )


def test_set_result():
    manager = MemoryManager()

    manager.set_result("RES-001")

    assert (
        manager.get_memory().current_result_id
        == "RES-001"
    )


def test_add_context():
    manager = MemoryManager()

    manager.add_context("language", "python")

    assert (
        manager.get_memory().active_context["language"]
        == "python"
    )


def test_clear():
    manager = MemoryManager()

    manager.set_user_request("Test")
    manager.clear()

    assert (
        manager.get_memory().current_user_request
        is None
    )


def test_health_check():
    manager = MemoryManager()

    health = manager.health_check()

    assert health["memory_manager"] is True