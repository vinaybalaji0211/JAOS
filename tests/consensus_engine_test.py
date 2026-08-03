from brain.consensus_engine import ConsensusEngine

engine = (
    ConsensusEngine()
)

engine.vote(
    "Deploy Quantum Agent",
    "ResearchAgent",
    "YES"
)

engine.vote(
    "Deploy Quantum Agent",
    "SecurityAgent",
    "YES"
)

engine.vote(
    "Deploy Quantum Agent",
    "MemoryAgent",
    "NO"
)

engine.show_votes()