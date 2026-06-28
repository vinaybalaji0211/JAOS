import pytest

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.mission_manager import MissionManager
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.mission_model import MissionModel


def test_mission_manager_initializes():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    assert mission_manager.get_status() == "INITIALIZED"


def test_mission_manager_rejects_invalid_registry_manager():
    with pytest.raises(TypeError):
        MissionManager("not a registry manager")


def test_mission_manager_initialize():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    assert mission_manager.initialize() is True
    assert mission_manager.get_status() == "READY"


def test_mission_manager_health_check():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission_manager.initialize()

    assert mission_manager.health_check() == {
        "mission_manager": True,
        "registry_manager": True,
    }


def test_create_mission():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
        related_goal_id="GOAL-001",
    )

    assert isinstance(mission, MissionModel)
    assert mission.mission_name == "Build homepage"
    assert mission.related_goal_id == "GOAL-001"

    stored_mission = registry_manager.mission_registry.get_mission(
        mission.mission_id
    )

    assert stored_mission == mission


def test_create_mission_with_steps():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
        steps=[
            "Create navbar",
            "Create hero section",
            "Create footer",
        ],
    )

    assert mission.total_steps == 3
    assert mission.steps == [
        "Create navbar",
        "Create hero section",
        "Create footer",
    ]


def test_create_mission_with_metadata():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build dashboard",
        metadata={
            "priority": "high",
            "source": "test",
        },
    )

    assert mission.metadata["priority"] == "high"
    assert mission.metadata["source"] == "test"


def test_get_mission():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
    )

    assert mission_manager.get_mission(mission.mission_id) == mission


def test_list_missions():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
    )

    assert mission_manager.list_missions() == [mission]


def test_get_missions_by_goal():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
        related_goal_id="GOAL-001",
    )

    mission_manager.create_mission(
        mission_name="Build dashboard",
        related_goal_id="GOAL-002",
    )

    assert mission_manager.get_missions_by_goal("GOAL-001") == [mission]


def test_update_mission_status():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
    )

    updated_mission = mission_manager.update_mission_status(
        mission_id=mission.mission_id,
        status=LifecycleStatus.ACTIVE,
    )

    assert updated_mission.status == LifecycleStatus.ACTIVE


def test_update_mission_progress():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    mission = mission_manager.create_mission(
        mission_name="Build homepage",
    )

    updated_mission = mission_manager.update_mission_progress(
        mission_id=mission.mission_id,
        progress=75.0,
    )

    assert updated_mission.progress == 75.0


def test_update_missing_mission_status_raises_key_error():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    with pytest.raises(KeyError):
        mission_manager.update_mission_status(
            mission_id="MIS-DOES-NOT-EXIST",
            status=LifecycleStatus.ACTIVE,
        )


def test_update_missing_mission_progress_raises_key_error():
    registry_manager = RegistryManager()
    mission_manager = MissionManager(registry_manager)

    with pytest.raises(KeyError):
        mission_manager.update_mission_progress(
            mission_id="MIS-DOES-NOT-EXIST",
            progress=50.0,
        )