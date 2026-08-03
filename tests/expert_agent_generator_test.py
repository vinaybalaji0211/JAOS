from brain.expert_agent_generator import ExpertAgentGenerator

generator = (
    ExpertAgentGenerator()
)

generator.create_agent(
    "QuantumPhysicsAgent",
    [
        "Quantum Theory",
        "Wave Mechanics",
        "Quantum Computing"
    ]
)

generator.create_agent(
    "CyberSecurityAgent",
    [
        "Threat Analysis",
        "Intrusion Detection",
        "Security Auditing"
    ]
)

generator.show_agents()