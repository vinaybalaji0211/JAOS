import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.mission_model import MissionModel
from executive_brain.registries.mission_registry import MissionRegistry


def test_add_and_get_mission():
    registry = MissionRegistry()
    mission = MissionModel(mission_name="Build homepage")

    registry.add_mission(mission)

    assert registry.get_mission(mission.mission_id) == mission
    assert registry.count() == 1


def test_reject_non_mission_model():
    registry = MissionRegistry()

    with pytest.raises(TypeError):
        registry.add_mission("not a mission")


def test_reject_duplicate_mission():
    registry = MissionRegistry()
    mission = MissionModel(mission_name="Build homepage")

    registry.add_mission(mission)

    with pytest.raises(ValueError):
        registry.add_mission(mission)


def test_update_mission():
    registry = MissionRegistry()
    mission = MissionModel(mission_name="Build homepage")

    registry.add_mission(mission)

    mission.update_status(LifecycleStatus.ACTIVE)
    mission.update_progress(50.0)
    registry.update_mission(mission)

    updated = registry.get_mission(mission.mission_id)

    assert updated.status == LifecycleStatus.ACTIVE
    assert updated.progress == 50.0


def test_remove_mission():
    registry = MissionRegistry()
    mission = MissionModel(mission_name="Build homepage")

    registry.add_mission(mission)
    removed = registry.remove_mission(mission.mission_id)

    assert removed == mission
    assert registry.get_mission(mission.mission_id) is None
    assert registry.count() == 0


def test_get_by_status():
    registry = MissionRegistry()

    active_mission = MissionModel(
        mission_name="Build homepage",
        status=LifecycleStatus.ACTIVE,
    )

    completed_mission = MissionModel(
        mission_name="Build contact page",
        status=LifecycleStatus.COMPLETED,
    )

    registry.add_mission(active_mission)
    registry.add_mission(completed_mission)

    active = registry.get_by_status(LifecycleStatus.ACTIVE)

    assert active == [active_mission]


def test_get_by_goal():
    registry = MissionRegistry()

    mission_1 = MissionModel(
        mission_name="Build homepage",
        related_goal_id="GOAL-001",
    )

    mission_2 = MissionModel(
        mission_name="Build dashboard",
        related_goal_id="GOAL-002",
    )

    registry.add_mission(mission_1)
    registry.add_mission(mission_2)

    result = registry.get_by_goal("GOAL-001")

    assert result == [mission_1]


def test_get_active_missions():
    registry = MissionRegistry()

    active_mission = MissionModel(
        mission_name="Build homepage",
        status=LifecycleStatus.ACTIVE,
    )

    pending_mission = MissionModel(
        mission_name="Build dashboard",
        status=LifecycleStatus.PENDING,
    )

    registry.add_mission(active_mission)
    registry.add_mission(pending_mission)

    assert registry.get_active_missions() == [active_mission]


def test_get_completed_missions():
    registry = MissionRegistry()

    completed_mission = MissionModel(
        mission_name="Build homepage",
        status=LifecycleStatus.COMPLETED,
    )

    active_mission = MissionModel(
        mission_name="Build dashboard",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_mission(completed_mission)
    registry.add_mission(active_mission)

    assert registry.get_completed_missions() == [completed_mission]


def test_get_incomplete_missions():
    registry = MissionRegistry()

    completed_mission = MissionModel(
        mission_name="Build homepage",
        status=LifecycleStatus.COMPLETED,
    )

    active_mission = MissionModel(
        mission_name="Build dashboard",
        status=LifecycleStatus.ACTIVE,
    )

    registry.add_mission(completed_mission)
    registry.add_mission(active_mission)

    assert registry.get_incomplete_missions() == [active_mission]


def test_get_progress_above():
    registry = MissionRegistry()

    low_progress_mission = MissionModel(
        mission_name="Build homepage",
        progress=20.0,
    )

    high_progress_mission = MissionModel(
        mission_name="Build dashboard",
        progress=80.0,
    )

    registry.add_mission(low_progress_mission)
    registry.add_mission(high_progress_mission)

    result = registry.get_progress_above(50.0)

    assert result == [high_progress_mission]


def test_get_progress_above_rejects_invalid_value():
    registry = MissionRegistry()

    with pytest.raises(ValueError):
        registry.get_progress_above(150.0)