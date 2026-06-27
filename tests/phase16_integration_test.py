from brain.master_brain_agent import MasterBrainAgent
from brain.agent_registry import AgentRegistry
from brain.ai_provider_manager import AIProviderManager
from brain.dynamic_agent_assignment_engine import DynamicAgentAssignmentEngine
from brain.agent_coordinator import AgentCoordinator

from brain.coding_agent import CodingAgent
from brain.research_agent import ResearchAgent
from brain.memory_agent import MemoryAgent
from brain.document_agent import DocumentAgent
from brain.email_agent import EmailAgent
from brain.calendar_agent import CalendarAgent
from brain.pc_control_agent import PCControlAgent
from brain.vision_agent import VisionAgent
from brain.security_agent import SecurityAgent


print("\n=== PHASE 16 INTEGRATION TEST ===\n")

brain = MasterBrainAgent()
brain.register_agent("Coding Agent")
brain.register_agent("Research Agent")
brain.register_agent("Memory Agent")
brain.register_agent("Security Agent")
brain.receive_request("Analyze security and code quality")
brain.show_status()

registry = AgentRegistry()
registry.register_agent("Coding Agent", "coding", ["write_code", "debug_code"])
registry.register_agent("Research Agent", "research", ["web_research", "fact_checking"])
registry.register_agent("Security Agent", "security", ["threat_detection", "audit_logs"])
registry.show_agents()

providers = AIProviderManager()
providers.register_provider("OpenAI", ["reasoning", "coding", "vision"], "MEDIUM", "FAST", "HIGH")
providers.register_provider("Gemini", ["vision", "research", "conversation"], "MEDIUM", "FAST", "HIGH")
providers.show_providers()

DynamicAgentAssignmentEngine.show_assignments(
    "Gemini",
    ["vision", "research", "conversation"]
)

coordinator = AgentCoordinator()
coordinator.assign_task("Coding Agent", "Review code")
coordinator.assign_task("Security Agent", "Check risks")
coordinator.update_result("Coding Agent", "Code review accepted")
coordinator.update_result("Security Agent", "Security scan accepted")
coordinator.show_tasks()

agents = [
    CodingAgent(),
    ResearchAgent(),
    MemoryAgent(),
    DocumentAgent(),
    EmailAgent(),
    CalendarAgent(),
    PCControlAgent(),
    VisionAgent(),
    SecurityAgent()
]

print("\nSpecialized Agent Tests:\n")

for agent in agents:
    print(agent.name)
    if hasattr(agent, "handle_task"):
        print(agent.handle_task("Run general task"))
    print()

print("\n=== PHASE 16 COMPLETE ===")