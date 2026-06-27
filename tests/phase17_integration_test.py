from brain.knowledge_graph_core import KnowledgeGraphCore
from brain.knowledge_domain_manager import KnowledgeDomainManager
from brain.entity_manager import EntityManager
from brain.relationship_manager import RelationshipManager
from brain.knowledge_storage_engine import KnowledgeStorageEngine
from brain.knowledge_retrieval_engine import KnowledgeRetrievalEngine
from brain.knowledge_validation_engine import KnowledgeValidationEngine
from brain.knowledge_acquisition_engine import KnowledgeAcquisitionEngine
from brain.knowledge_gap_mapper import KnowledgeGapMapper
from brain.knowledge_importance_scorer import KnowledgeImportanceScorer


print("\n=== PHASE 17 INTEGRATION TEST ===\n")

graph = KnowledgeGraphCore()
graph.add_relationship("Vinay", "owns", "JARVIS")
graph.add_relationship("JARVIS", "contains", "Knowledge Graph")
graph.show_graph()

domains = KnowledgeDomainManager()
domains.add_domain("Physics", "Study of matter and energy.")
domains.add_topic("Physics", "Quantum Physics")
domains.show_domains()

entities = EntityManager()
entities.add_entity("Quantum Physics", "KNOWLEDGE_TOPIC", {"domain": "Physics"})
entities.show_entities()

relations = RelationshipManager()
relations.add_relationship("Quantum Physics", "belongs_to", "Physics")
relations.show_relationships()

storage = KnowledgeStorageEngine()
storage.store_entity("Quantum Physics")
storage.store_domain("Physics")
storage.store_relationship({
    "source": "Quantum Physics",
    "relation": "belongs_to",
    "target": "Physics"
})
storage.show_storage()

retrieval = KnowledgeRetrievalEngine()
retrieval.add_knowledge("Quantum Physics belongs to Physics")
retrieval.add_knowledge("Security Threat Response Engine protects JARVIS")
retrieval.show_search("physics")

KnowledgeValidationEngine.show_validation(
    "Verified and trusted Quantum Physics note"
)

acquisition = KnowledgeAcquisitionEngine()
acquisition.acquire_subject("Quantum Physics", "Physics")
acquisition.show_learning_targets()

gap = KnowledgeGapMapper()
gap.define_domain(
    "Physics",
    [
        "Quantum Physics",
        "Electromagnetism",
        "Thermodynamics"
    ]
)
gap.add_known_topic("Physics", "Quantum Physics")
gap.show_gaps("Physics")

KnowledgeImportanceScorer.show_score(
    "Quantum Physics learning roadmap"
)

print("\n=== PHASE 17 COMPLETE ===")