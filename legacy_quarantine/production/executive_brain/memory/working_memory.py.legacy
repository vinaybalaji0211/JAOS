from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkingMemory:
    current_user_request: str | None = None
    current_mission_id: str | None = None
    current_execution_plan_id: str | None = None
    current_decision_id: str | None = None
    current_result_id: str | None = None
    active_context: dict = field(default_factory=dict)
    updated_at: datetime = field(default_factory=datetime.now)

    def set_user_request(self, request: str):
        if not request.strip():
            raise ValueError("request cannot be empty.")
        self.current_user_request = request
        self.updated_at = datetime.now()

    def set_mission(self, mission_id: str):
        self.current_mission_id = mission_id
        self.updated_at = datetime.now()

    def set_execution_plan(self, execution_plan_id: str):
        self.current_execution_plan_id = execution_plan_id
        self.updated_at = datetime.now()

    def set_decision(self, decision_id: str):
        self.current_decision_id = decision_id
        self.updated_at = datetime.now()

    def set_result(self, result_id: str):
        self.current_result_id = result_id
        self.updated_at = datetime.now()

    def add_context(self, key, value):
        self.active_context[key] = value
        self.updated_at = datetime.now()

    def clear(self):
        self.current_user_request = None
        self.current_mission_id = None
        self.current_execution_plan_id = None
        self.current_decision_id = None
        self.current_result_id = None
        self.active_context.clear()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "current_user_request": self.current_user_request,
            "current_mission_id": self.current_mission_id,
            "current_execution_plan_id": self.current_execution_plan_id,
            "current_decision_id": self.current_decision_id,
            "current_result_id": self.current_result_id,
            "active_context": self.active_context,
            "updated_at": self.updated_at.isoformat(),
        }