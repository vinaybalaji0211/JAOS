from brain.agent_blueprint_designer import AgentBlueprintDesigner
from brain.agent_deployment_manager import AgentDeploymentManager
from brain.agent_lifecycle_manager import AgentLifecycleManager
from brain.agent_training_manager import AgentTrainingManager
from brain.autonomous_agent_creation_planner import AutonomousAgentCreationPlanner
from brain.expert_agent_generator import ExpertAgentGenerator

print(
    "\n=== EXPERT AGENT INTEGRATION TEST ===\n"
)

# Proposal

planner = (
    AutonomousAgentCreationPlanner()
)

planner.create_proposal(
    "QuantumPhysicsAgent",
    "Advanced quantum research"
)

planner.approve_proposal(
    "QuantumPhysicsAgent"
)

planner.show_proposals()

# Blueprint

designer = (
    AgentBlueprintDesigner()
)

designer.create_blueprint(
    "QuantumPhysicsAgent",
    "Quantum Physics Expert",
    [
        "Quantum Theory",
        "Wave Mechanics"
    ],
    [
        "READ_KNOWLEDGE"
    ],
    [
        "KnowledgeGraph"
    ]
)

designer.show_blueprints()

# Generator

generator = (
    ExpertAgentGenerator()
)

generator.create_agent(
    "QuantumPhysicsAgent",
    [
        "Quantum Theory",
        "Wave Mechanics"
    ]
)

generator.show_agents()

# Training

training = (
    AgentTrainingManager()
)

training.start_training(
    "QuantumPhysicsAgent",
    [
        "Quantum Theory",
        "Wave Mechanics"
    ]
)

training.update_progress(
    "QuantumPhysicsAgent",
    100
)

training.show_training()

# Deployment

deployment = (
    AgentDeploymentManager()
)

deployment.deploy_agent(
    "QuantumPhysicsAgent"
)

deployment.activate_agent(
    "QuantumPhysicsAgent"
)

deployment.show_agents()

# Lifecycle

lifecycle = (
    AgentLifecycleManager()
)

lifecycle.create_agent(
    "QuantumPhysicsAgent"
)

lifecycle.update_status(
    "QuantumPhysicsAgent",
    "ACTIVE"
)

lifecycle.show_agents()

print(
    "\n=== EXPERT AGENT SYSTEM COMPLETE ==="
)