from brain.evolution_memory import (
    EvolutionMemory
)

memory = EvolutionMemory()

memory.record_event(
    "UPGRADE_PROPOSED",
    "Cloud Memory Architecture proposed."
)

memory.record_event(
    "UPGRADE_APPROVED",
    "Cloud Memory Architecture approved."
)

memory.record_event(
    "UPGRADE_DEPLOYED",
    "Cloud Memory Architecture deployed."
)

memory.record_event(
    "UPGRADE_SUCCESS",
    "Cloud Memory Architecture working successfully."
)

memory.show_history()