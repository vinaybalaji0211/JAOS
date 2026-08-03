from infrastructure.intelligent_resource_orchestrator import (
    IntelligentResourceOrchestrator,
)

iro = IntelligentResourceOrchestrator()

iro.register_resource(
    "OpenAI",
    "AI Provider",
    "READY"
)

iro.register_resource(
    "GitHub",
    "Integration",
    "READY"
)

iro.register_resource(
    "Local LLM",
    "AI Provider",
    "OFFLINE"
)

iro.register_resource(
    "Docker",
    "Tool",
    "READY"
)

iro.show_resources()

print(
    iro.get_resource("GitHub")
)