from brain.vision_agent import VisionAgent

agent = VisionAgent()

agent.show_capabilities()

print()

print(
    agent.handle_task(
        "Analyze image"
    )
)

print(
    agent.handle_task(
        "Run OCR on document"
    )
)

print(
    agent.handle_task(
        "Understand screen contents"
    )
)