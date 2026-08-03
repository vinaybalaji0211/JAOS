from brain.decision_analysis_engine import DecisionAnalysisEngine

engine = (
    DecisionAnalysisEngine()
)

engine.analyze(
    "Choose Database",
    [
        "SQLite",
        "PostgreSQL",
        "MongoDB"
    ],
    "PostgreSQL"
)

engine.analyze(
    "Choose AI Provider",
    [
        "OpenAI",
        "Gemini",
        "Local LLM"
    ],
    "OpenAI"
)

engine.show_decisions()