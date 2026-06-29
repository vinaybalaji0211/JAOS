"""
JAOS Component: MemoryManager

Purpose:
    Manage the WorkingMemory lifecycle.

Responsibilities:
    - Initialize working memory
    - Update working memory
    - Clear working memory
    - Provide access to current working memory

Non-Responsibilities:
    - Long-term memory
    - AI reasoning
    - Memory ranking
"""

from executive_brain.memory.working_memory import WorkingMemory
from executive_brain.memory.memory_registry import MemoryRegistry


class MemoryManager:
    """Manager responsible for WorkingMemory."""

    def __init__(self):
        self.registry = MemoryRegistry()
        self.initialize()

    def initialize(self):
        if not self.registry.has_memory():
            self.registry.add_memory(WorkingMemory())

    def get_memory(self):
        return self.registry.get_memory()

    def clear(self):
        self.get_memory().clear()

    def set_user_request(self, request: str):
        self.get_memory().set_user_request(request)

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