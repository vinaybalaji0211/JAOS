"""
JAOS Component: ExecutiveBrain

Purpose:
    Central coordinator for the JAOS Executive Brain.

Responsibilities:
    - Initialize executive subsystems
    - Coordinate managers
    - Report executive health
    - Provide a single entry point for future reasoning

Non-Responsibilities:
    - AI reasoning
    - Memory management
    - Tool execution
"""

from executive_brain.managers.registry_manager import RegistryManager


class ExecutiveBrain:
    """Central coordination component of JAOS."""

    VERSION = "0.5.0-dev"

    def __init__(self):
        self.registry_manager = RegistryManager()

        self.status = "INITIALIZED"

    def initialize(self):
        self.status = "READY"
        return True

    def get_status(self):
        return self.status

    def get_registry_manager(self):
        return self.registry_manager

    def get_system_summary(self):
        return {
            "status": self.status,
            "version": self.VERSION,
            "registry_manager": self.registry_manager is not None,
            "registries": self.registry_manager.list_registries(),
            "registry_counts": self.registry_manager.registry_counts(),
        }

    def health_check(self):
        return {
            "executive_brain": self.status == "READY",
            "registry_manager": self.registry_manager.health_check(),
        }