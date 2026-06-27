from brain.decision_engine import DecisionEngine


options = [
    {
        "name": "Use OpenAI",
        "priority": 20,
        "confidence": 90,
        "goal_alignment": 80,
        "resources_ok": True,
        "risk": "LOW"
    },
    {
        "name": "Use Unknown Plugin",
        "priority": 30,
        "confidence": 50,
        "goal_alignment": 40,
        "resources_ok": True,
        "risk": "HIGH"
    },
    {
        "name": "Run blocked command",
        "priority": 100,
        "confidence": 90,
        "goal_alignment": 20,
        "resources_ok": True,
        "risk": "BLOCKED"
    }
]

DecisionEngine.show_decision(options)