from brain.action_execution_engine import ActionExecutionEngine

engine = (
    ActionExecutionEngine()
)

result = engine.execute(
    "ReadKnowledgeGraph",
    "Knowledge loaded successfully"
)

print(result)

engine.execute(
    "GenerateReport",
    "Report created"
)

engine.show_history()