from brain.agent_deployment_manager import AgentDeploymentManager

manager = (
    AgentDeploymentManager()
)

manager.deploy_agent(
    "QuantumPhysicsAgent"
)

manager.deploy_agent(
    "CyberSecurityAgent"
)

manager.activate_agent(
    "QuantumPhysicsAgent"
)

manager.show_agents()