from infrastructure.infrastructure_intelligence_core import (
    InfrastructureIntelligenceCore
)

from infrastructure.ai_provider_manager import (
    AIProviderManager
)

from infrastructure.intelligent_resource_orchestrator import (
    IntelligentResourceOrchestrator
)

from infrastructure.multi_provider_task_composer import (
    MultiProviderTaskComposer
)

from infrastructure.api_intelligence_manager import (
    APIIntelligenceManager
)

from infrastructure.storage_intelligence import (
    StorageIntelligence
)

from infrastructure.database_intelligence import (
    DatabaseIntelligence
)

from infrastructure.cost_performance_optimizer import (
    CostPerformanceOptimizer
)

print("\n===== INFRASTRUCTURE PLATFORM TEST =====\n")

core = InfrastructureIntelligenceCore()
core.register_component(
    "Infrastructure Core",
    "READY"
)

providers = AIProviderManager()
providers.register_provider(
    "OpenAI",
    "READY"
)

iro = IntelligentResourceOrchestrator()
iro.register_resource(
    "GitHub",
    "Integration",
    "READY"
)

composer = MultiProviderTaskComposer()
composer.add_step(
    "Planner Agent",
    "Create execution plan"
)

api = APIIntelligenceManager()
api.register_api(
    "Gemini",
    "READY",
    "Unlimited",
    "Cloud"
)

storage = StorageIntelligence()
storage.register_storage(
    "Local Disk",
    "LOCAL",
    "READY"
)

database = DatabaseIntelligence()
database.register_database(
    "PostgreSQL",
    "RELATIONAL",
    "READY"
)

optimizer = CostPerformanceOptimizer()
optimizer.register_resource(
    "Local",
    0,
    80
)

print("\n===== COMPONENT STATUS =====\n")

core.show_components()
providers.show_providers()
iro.show_resources()
composer.show_plan()
api.show_apis()
storage.show_storage()
database.show_databases()
optimizer.show_resources()

print("\n===== INFRASTRUCTURE PLATFORM COMPLETE =====")