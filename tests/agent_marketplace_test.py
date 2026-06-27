from brain.agent_marketplace import AgentMarketplace


market = AgentMarketplace()

market.add_agent("Coder Agent", "1.0", "coding")
market.add_agent("Research Agent", "1.0", "research")
market.add_agent("Security Agent", "1.0", "security")

market.show_agents()

market.remove_agent("Research Agent")

market.show_agents()