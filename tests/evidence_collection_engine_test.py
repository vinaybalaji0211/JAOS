from brain.evidence_collection_engine import EvidenceCollectionEngine

engine = (
    EvidenceCollectionEngine()
)

engine.collect(
    "Unauthorized Upgrade Attempt",
    "Request originated from unknown source."
)

engine.collect(
    "Memory Tampering",
    "Critical memory record modified."
)

engine.show_evidence()