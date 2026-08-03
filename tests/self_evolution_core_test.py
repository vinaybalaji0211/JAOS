from brain.self_evolution_core import SelfEvolutionCore

core = SelfEvolutionCore()

core.propose_upgrade(
    "Cloud Memory Architecture",
    "Local disk storage is not scalable."
)

core.propose_upgrade(
    "Security Threat Response Engine",
    "JARVIS must respond to attack attempts."
)

core.show_status()

core.approve_upgrade(
    "Cloud Memory Architecture"
)

core.reject_upgrade(
    "Security Threat Response Engine"
)

core.show_status()