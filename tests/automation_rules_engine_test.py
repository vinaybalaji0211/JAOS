from workflow.automation_rules_engine import AutomationRulesEngine

engine = AutomationRulesEngine()

engine.add_rule(
    "Daily 08:00",
    "Summarize Emails"
)

engine.add_rule(
    "GitHub Push",
    "Run Tests"
)

engine.add_rule(
    "Battery <20%",
    "Pause Heavy Workflows"
)

engine.show_rules()