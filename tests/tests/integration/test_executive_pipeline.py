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


def test_multiple_requests():
    brain = ExecutiveBrain()
    brain.initialize()

    brain.execute("Task One")
    brain.execute("Task Two")

    summary = brain.get_system_summary()
    counts = summary["registry_counts"]

    assert counts["mission"] == 2
    assert counts["execution_plan"] == 2
    assert counts["decision"] == 2
    assert counts["result"] == 2


def test_empty_request():
    brain = ExecutiveBrain()
    brain.initialize()

    with pytest.raises(ValueError):
        brain.execute("")