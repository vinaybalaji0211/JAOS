from brain.research_agent import ResearchAgent

agent = ResearchAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Fact check this information"
    )
)

print(
    agent.handle_task(
        "Do competitor analysis"
    )
)

print(
    agent.handle_task(
        "Create market research report"
    )
)