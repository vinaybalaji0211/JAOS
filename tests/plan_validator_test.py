from brain.plan_validator import PlanValidator


plan = [
    "Understand the task",
    "Break task into steps",
    "Check capabilities",
    "Validate safety"
]

matched_capabilities = [
    "planning",
    "reasoning"
]

missing_capabilities = []

risk_level = "LOW"

execution_strategy = "SEQUENTIAL"

PlanValidator.show_validation(
    plan,
    matched_capabilities,
    missing_capabilities,
    risk_level,
    execution_strategy
)

print("\n--- Invalid Plan Test ---")

PlanValidator.show_validation(
    [],
    [],
    [
        "vision"
    ],
    "HIGH",
    None
)