"""
JAOS Component: ExecutiveBrain

Purpose:
    Central coordinator for the JAOS Executive Brain.

Responsibilities:
    - Initialize executive subsystems
    - Coordinate managers
    - Maintain working memory
    - Report executive health
    - Provide a single entry point for orchestration
    - Integrate with the JAOS Platform Runtime

Non-Responsibilities:
    - AI reasoning
    - Long-term memory management
    - Real tool execution
"""

from executive_brain.managers.decision_manager import DecisionManager
from executive_brain.managers.execution_manager import ExecutionManager
from executive_brain.managers.mission_manager import MissionManager
from executive_brain.managers.planning_manager import PlanningManager
from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.managers.result_manager import ResultManager
from executive_brain.memory.memory_manager import MemoryManager
from jaos_platform.platform_runtime import PlatformRuntime


class ExecutiveBrain:
    """Central coordination component of JAOS."""

    VERSION = "0.5.0-dev"

    def __init__(self, runtime: PlatformRuntime | None = None):
        self.runtime = runtime or PlatformRuntime()

        self.registry_manager = RegistryManager()

        if self.runtime.container.is_registered("memory_manager"):
            self.memory_manager = self.runtime.container.resolve(
                "memory_manager"
            )
        else:
            self.memory_manager = MemoryManager(self.runtime)

        self.planning_manager = PlanningManager(self.registry_manager)
        self.decision_manager = DecisionManager(self.registry_manager)
        self.mission_manager = MissionManager(self.registry_manager)
        self.execution_manager = ExecutionManager(self.registry_manager)
        self.result_manager = ResultManager(self.registry_manager)

        self.status = "INITIALIZED"

        self.runtime.container.register("executive_brain", self)
        self.runtime.context.set("executive_brain_status", self.status)
        self.runtime.events.publish(
            "executive_brain_initialized",
            {"status": self.status},
        )

    def initialize(self):
        self.planning_manager.initialize()
        self.decision_manager.initialize()
        self.mission_manager.initialize()
        self.execution_manager.initialize()
        self.result_manager.initialize()

        self.status = "READY"

        self.runtime.context.set("executive_brain_status", self.status)
        self.runtime.events.publish(
            "executive_brain_ready",
            {"status": self.status},
        )

        return True

    def get_status(self):
        return self.status

    def get_registry_manager(self):
        return self.registry_manager

    def get_memory_manager(self):
        return self.memory_manager

    def execute(self, user_request: str):
        if not user_request.strip():
            raise ValueError("user_request cannot be empty.")

        self.memory_manager.clear()
        self.memory_manager.set_user_request(user_request)

        mission = self.mission_manager.create_mission(
            mission_name=user_request,
            metadata={
                "source": "executive_pipeline",
            },
        )
        self.memory_manager.set_mission(mission.mission_id)

        execution_plan = self.planning_manager.create_execution_plan(
            target_platform="jaos",
            target_service="simulated_execution",
            related_mission_id=mission.mission_id,
            metadata={
                "user_request": user_request,
                "pipeline": "executive_brain",
            },
        )
        self.memory_manager.set_execution_plan(
            execution_plan.execution_plan_id
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
        self.memory_manager.set_decision(decision.decision_id)

        result = self.execution_manager.execute_plan(
            execution_plan.execution_plan_id
        )

        result.add_metadata("decision_id", decision.decision_id)
        result.add_metadata("mission_id", mission.mission_id)
        result.add_metadata("user_request", user_request)

        self.memory_manager.set_result(result.result_id)
        self.memory_manager.add_context("last_result_success", result.success)

        return result

    def get_system_summary(self):
        return {
            "status": self.status,
            "version": self.VERSION,
            "registry_manager": self.registry_manager is not None,
            "memory_manager": self.memory_manager.get_status(),
            "registries": self.registry_manager.list_registries(),
            "registry_counts": self.registry_manager.registry_counts(),
            "working_memory": self.memory_manager.get_memory().to_dict(),
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
            "memory_manager": self.memory_manager.health_check(),
            "planning_manager": self.planning_manager.health_check(),
            "decision_manager": self.decision_manager.health_check(),
            "mission_manager": self.mission_manager.health_check(),
            "execution_manager": self.execution_manager.health_check(),
            "result_manager": self.result_manager.health_check(),
        }