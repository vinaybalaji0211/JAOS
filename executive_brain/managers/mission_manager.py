"""
JAOS Component: MissionManager

Purpose:
    Create and manage missions inside the Executive Brain.

Responsibilities:
    - Create MissionModel objects
    - Store missions through RegistryManager
    - Retrieve missions
    - Update mission progress
    - Report manager status and health

Non-Responsibilities:
    - Execute missions
    - Make AI decisions
    - Create execution plans
    - Manage memory
"""

from executive_brain.common.enums import LifecycleStatus
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.mission_model import MissionModel


class MissionManager:
    """Manager responsible for creating and registering missions."""

    def __init__(self, registry_manager: RegistryManager):
        if not isinstance(registry_manager, RegistryManager):
            raise TypeError(
                "registry_manager must be an instance of RegistryManager."
            )

        self.registry_manager = registry_manager
        self.status = "INITIALIZED"

    def initialize(self):
        self.status = "READY"
        return True

    def get_status(self):
        return self.status

    def health_check(self):
        return {
            "mission_manager": self.status == "READY",
            "registry_manager": self.registry_manager is not None,
        }

    def create_mission(
        self,
        mission_name: str,
        related_goal_id: str | None = None,
        steps: list | None = None,
        metadata: dict | None = None,
    ):
        mission_steps = steps or []

        mission = MissionModel(
            mission_name=mission_name,
            status=LifecycleStatus.CREATED,
            related_goal_id=related_goal_id,
            steps=mission_steps,
            total_steps=len(mission_steps),
        )

        if metadata:
            for key, value in metadata.items():
                mission.add_metadata(key, value)

        self.registry_manager.mission_registry.add_mission(mission)

        return mission

    def get_mission(self, mission_id: str):
        return self.registry_manager.mission_registry.get_mission(mission_id)

    def list_missions(self):
        return self.registry_manager.mission_registry.list_missions()

    def get_missions_by_goal(self, goal_id: str):
        return self.registry_manager.mission_registry.get_by_goal(goal_id)

    def update_mission_status(
        self,
        mission_id: str,
        status: LifecycleStatus,
    ):
        mission = self.get_mission(mission_id)

        if mission is None:
            raise KeyError(f"Mission not found: {mission_id}")

        mission.update_status(status)
        self.registry_manager.mission_registry.update_mission(mission)

        return mission

    def update_mission_progress(
        self,
        mission_id: str,
        progress: float,
    ):
        mission = self.get_mission(mission_id)

        if mission is None:
            raise KeyError(f"Mission not found: {mission_id}")

        mission.update_progress(progress)
        self.registry_manager.mission_registry.update_mission(mission)

        return mission