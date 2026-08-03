from brain.context_intelligence import ContextIntelligence

context = {
    "current_phase": "Phase 3",
    "current_goal": "Build memory and brain architecture"
}

result = ContextIntelligence.analyze(
    context
)

print(result)