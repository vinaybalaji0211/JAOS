from brain.document_agent import DocumentAgent

agent = DocumentAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Analyze this PDF"
    )
)

print(
    agent.handle_task(
        "Extract key information"
    )
)

print(
    agent.handle_task(
        "Generate summary report"
    )
)