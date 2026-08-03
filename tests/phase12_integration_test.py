from brain.agent_marketplace import AgentMarketplace
from brain.author_approval_lock import AuthorApprovalLock
from brain.command_risk_scanner import CommandRiskScanner
from brain.dependency_manager import DependencyManager
from brain.intrusion_alert_system import IntrusionAlertSystem
from brain.plugin_manager import PluginManager
from brain.plugin_registry import PluginRegistry
from brain.plugin_trust_manager import PluginTrustManager
from brain.security_lockdown_mode import SecurityLockdownMode
from brain.skill_marketplace import SkillMarketplace

print("\n=== PHASE 12 INTEGRATION TEST ===\n")

# Plugin Manager
plugins = PluginManager()
plugins.load_plugin(
    "Weather Plugin"
)
plugins.show_plugins()

# Registry
registry = PluginRegistry()
registry.register_plugin(
    "Weather Plugin",
    "1.0",
    "Vinay",
    trust_score=85
)
registry.show_plugins()

# Trust
PluginTrustManager.show_decision(
    registry.get_plugin(
        "Weather Plugin"
    )
)

# Command Scan
CommandRiskScanner.show_scan(
    "pip install requests"
)

# Author Lock
AuthorApprovalLock.show_access(
    "Vinay",
    "architecture",
    True
)

# Intrusion
IntrusionAlertSystem.show_alert(
    "failed_login"
)

# Lockdown
lockdown = SecurityLockdownMode()
lockdown.enter_lockdown()
lockdown.show_status()

# Skills
skills = SkillMarketplace()
skills.add_skill(
    "Translator Skill",
    "1.0"
)
skills.show_skills()

# Agents
agents = AgentMarketplace()
agents.add_agent(
    "Research Agent",
    "1.0",
    "research"
)
agents.show_agents()

# Dependencies
deps = DependencyManager()
deps.add_dependency(
    "requests",
    "2.31.0",
    "2.31.0"
)
deps.show_dependencies()

print("\n=== PHASE 12 COMPLETE ===")