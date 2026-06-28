"""
JAOS Component: ExecutiveBrain

Purpose:
    Central coordinator for the JAOS Executive Brain.

Responsibilities:
    - Initialize executive subsystems
    - Coordinate managers
    - Report executive health
    - Provide a single entry point for orchestration

Non-Responsibilities:
    - AI reasoning
    - Memory management
    - Real tool execution
"""

from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.managers.planning_manager import PlanningManager
from executive_brain.managers.decision_manager import DecisionManager
from executive_brain.managers.mission_manager import MissionManager
from executive_brain.managers.execution_manager import ExecutionManager
from executive_brain.managers.result_manager import ResultManager


class ExecutiveBrain:
    """Central coordination component of JAOS."""

    VERSION = "0.5.0-dev"

    def __init__(self):
        self.registry_manager = RegistryManager()
        self.planning_manager = PlanningManager(self.registry_manager)
        self.decision_manager = DecisionManager(self.registry_manager)
        self.mission_manager = MissionManager(self.registry_manager)
        self.execution_manager = ExecutionManager(self.registry_manager)
        self.result_manager = ResultManager(self.registry_manager)

        self.status = "INITIALIZED"

    def initialize(self):
        self.planning_manager.initialize()
        self.decision_manager.initialize()
        self.mission_manager.initialize()
        self.execution_manager.initialize()
        self.result_manager.initialize()

        self.status = "READY"
        return True

    def get_status(self):
        return self.status

    def get_registry_manager(self):
        return self.registry_manager

    def execute(self, user_request: str):
        if not user_request.strip():
            raise ValueError("user_request cannot be empty.")

        mission = self.mission_manager.create_mission(
            mission_name=user_request,
            metadata={
                "source": "executive_pipeline",
            },
        )

        execution_plan = self.planning_manager.create_execution_plan(
            target_platform="jaos",
            target_service="simulated_execution",
            related_mission_id=mission.mission_id,
            metadata={
                "user_request": user_request,
                "pipeline": "executive_brain",
            },
        )

        decision = self.decision_manager.create_decision(
            decision_type="approve_execution",
            reason="Alpha pipeline approves simulated execution.",
            confidence=1.0,
            metadata={
                "mission_id": mission.mission_id,
                "execution_plan_id": execution_plan.execution_plan_id,
            },
        )

        result = self.execution_manager.execute_plan(
            execution_plan.execution_plan_id
        )

        result.add_metadata("decision_id", decision.decision_id)
        result.add_metadata("mission_id", mission.mission_id)
        result.add_metadata("user_request", user_request)

        return result

    def get_system_summary(self):
        return {
            "status": self.status,
            "version": self.VERSION,
            "registry_manager": self.registry_manager is not None,
            "registries": self.registry_manager.list_registries(),
            "registry_counts": self.registry_manager.registry_counts(),
            "managers": {
                "planning_manager": self.planning_manager.get_status(),
                "decision_manager": self.decision_manager.get_status(),
                "mission_manager": self.mission_manager.get_status(),
                "execution_manager": self.execution_manager.get_status(),
                "result_manager": self.result_manager.get_status(),
            },
        }

    def health_check(self):
        return {
            "executive_brain": self.status == "READY",
            "registry_manager": self.registry_manager.health_check(),
            "planning_manager": self.planning_manager.health_check(),
            "decision_manager": self.decision_manager.health_check(),
            "mission_manager": self.mission_manager.health_check(),
            "execution_manager": self.execution_manager.health_check(),
            "result_manager": self.result_manager.health_check(),
        }