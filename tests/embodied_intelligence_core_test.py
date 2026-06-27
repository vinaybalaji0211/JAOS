from brain.embodied_intelligence_core import (
    EmbodiedIntelligenceCore
)

core = EmbodiedIntelligenceCore()

core.set_environment(
    "Windows Desktop"
)

core.register_skill(
    "Application Control"
)

core.register_skill(
    "Workflow Observation"
)

core.register_skill(
    "Task Planning"
)

core.show_status()