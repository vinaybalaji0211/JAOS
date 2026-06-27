from brain.decision_record import DecisionRecord


DecisionRecord.record(
    "Use Planner Engine",
    "The user gave a goal that requires step-by-step planning",
    "HIGH"
)

DecisionRecord.record(
    "Use Reasoning Engine",
    "The plan needs high-level reasoning before validation",
    "HIGH"
)

DecisionRecord.show()