from core.agent_manager import AgentManager

manager = AgentManager()

manager.register_agent(
    "Memory Agent"
)

manager.register_agent(
    "Planner Agent"
)

manager.register_agent(
    "Tool Agent"
)

manager.register_agent(
    "Security Agent"
)

manager.show_agents()