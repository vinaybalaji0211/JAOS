from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.mission_model import MissionModel
from executive_brain.registries.base_registry import BaseRegistry


class MissionRegistry(BaseRegistry):
    """
    Registry responsible for storing and managing MissionModel objects.

    Responsibilities:
    - Store missions
    - Retrieve missions
    - Update missions
    - Remove missions
    - Filter missions

    Non-Responsibilities:
    - Execute missions
    - Make decisions
    - Create execution plans
    """

    def __init__(self):
        super().__init__()

    # ----------------------------
    # CRUD Operations
    # ----------------------------

    def add_mission(self, mission: MissionModel):
        if not isinstance(mission, MissionModel):
            raise TypeError(
                "mission must be an instance of MissionModel."
            )

        self.add(mission.mission_id, mission)

    def get_mission(self, mission_id: str):
        return self.get(mission_id)

    def update_mission(self, mission: MissionModel):
        if not isinstance(mission, MissionModel):
            raise TypeError(
                "mission must be an instance of MissionModel."
            )

        self.update(mission.mission_id, mission)

    def remove_mission(self, mission_id: str):
        return self.remove(mission_id)

    def list_missions(self):
        return self.list_all()

    # ----------------------------
    # Filters
    # ----------------------------

    def get_by_status(self, status: LifecycleStatus):
        return [
            mission
            for mission in self.list_all()
            if mission.status == status
        ]

    def get_by_goal(self, goal_id: str):
        return [
            mission
            for mission in self.list_all()
            if mission.related_goal_id == goal_id
        ]

    def get_active_missions(self):
        return self.get_by_status(
            LifecycleStatus.ACTIVE
        )

    def get_completed_missions(self):
        return self.get_by_status(
            LifecycleStatus.COMPLETED
        )

    def get_incomplete_missions(self):
        return [
            mission
            for mission in self.list_all()
            if mission.status != LifecycleStatus.COMPLETED
        ]

    def get_progress_above(self, progress: float):
        if not 0 <= progress <= 100:
            raise ValueError(
                "progress must be between 0 and 100."
            )

        return [
            mission
            for mission in self.list_all()
            if mission.progress >= progress
        ]