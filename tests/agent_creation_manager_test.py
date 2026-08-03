from brain.agent_creation_manager import AgentCreationManager

manager = AgentCreationManager()

manager.create_agent(
    "Pet Care Agent",
    "Assist with puppy care and pet health reminders",
    [
        "pet_advice",
        "feeding_schedule",
        "health_warning_detection"
    ]
)

manager.create_agent(
    "Finance Planning Agent",
    "Assist with budget and financial planning",
    [
        "budget_tracking",
        "expense_analysis",
        "financial_summary"
    ]
)

manager.show_created_agents()