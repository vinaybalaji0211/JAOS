"""
JAOS Component: MemoryManager

Purpose:
    Manage the WorkingMemory lifecycle.

Responsibilities:
    - Initialize working memory
    - Update working memory
    - Clear working memory
    - Provide access to current working memory
    - Integrate with JAOS Platform Runtime

Non-Responsibilities:
    - Long-term memory
    - AI reasoning
    - Memory ranking
"""

from jaos_platform.base_platform_service import BasePlatformService

from executive_brain.memory.working_memory import WorkingMemory
from executive_brain.memory.memory_registry import MemoryRegistry


class MemoryManager(BasePlatformService):
    """Manager responsible for WorkingMemory."""

    SERVICE_NAME = "memory_manager"

    def __init__(self, runtime=None):
        self.registry = MemoryRegistry()

        super().__init__(runtime)

        self.initialize()

    def initialize(self):
        if not self.registry.has_memory():
            self.registry.add_memory(WorkingMemory())

    def get_memory(self):
        return self.registry.get_memory()

    def clear(self):
        self.get_memory().clear()

        if self.runtime is not None:
            self.runtime.events.publish(
                "memory_cleared",
                {},
            )

    def set_user_request(self, request: str):
        self.get_memory().set_user_request(request)

        if self.runtime is not None:
            self.runtime.events.publish(
                "memory_user_request_set",
                {
                    "request": request,
                },
            )

    def set_mission(self, mission_id: str):
        self.get_memory().set_mission(mission_id)

    def set_execution_plan(self, execution_plan_id: str):
        self.get_memory().set_execution_plan(execution_plan_id)

    def set_decision(self, decision_id: str):
        self.get_memory().set_decision(decision_id)

    def set_result(self, result_id: str):
        self.get_memory().set_result(result_id)

    def add_context(self, key, value):
        self.get_memory().add_context(key, value)

    def health_check(self):
        return {
            "memory_manager": self.registry.has_memory()
        }

    def get_status(self):
        return "READY" if self.registry.has_memory() else "NOT_READY"