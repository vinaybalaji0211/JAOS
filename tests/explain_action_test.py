from core.explain_action import ExplainAction


explainer = ExplainAction()

explainer.record(
    "Created backup",
    "To protect project data from loss"
)

explainer.record(
    "Checked permissions",
    "To prevent unsafe actions"
)

explainer.show_explanations()