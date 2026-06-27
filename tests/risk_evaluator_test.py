from brain.risk_evaluator import RiskEvaluator


RiskEvaluator.show_risk(
    [
        "read_file",
        "memory_change"
    ]
)

RiskEvaluator.show_risk(
    [
        "web_access",
        "automation"
    ]
)

RiskEvaluator.show_risk(
    [
        "delete_file",
        "system_command"
    ]
)