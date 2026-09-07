"""
JAOS Component: Kernel

Purpose:
    Bootstrap and coordinate the JAOS system.

Responsibilities:
    - Initialize core services
    - Initialize RegistryManager
    - Report system status
    - Provide startup information

Non-Responsibilities:
    - AI reasoning
    - Planning
    - Mission execution
    - Memory management
"""

from datetime import datetime

from executive_brain.managers.registry_manager import RegistryManager


class JAOSKernel:
    """Central bootstrapper for the JAOS AI Operating System."""

    VERSION = "0.5.0-dev"

    def __init__(self):
        self.started_at = None
        self.registry_manager = None
        self.system_status = "OFFLINE"

    def boot(self):
        """Boot the JAOS kernel."""

        print("=" * 55)
        print(" JAOS AI Operating System")
        print(f" Version: {self.VERSION}")
        print("=" * 55)

        self.started_at = datetime.now()

        print("[✓] Booting Kernel...")

        self.registry_manager = RegistryManager()
        print("[✓] RegistryManager Ready")

        self.system_status = "ONLINE"

        print("[✓] Kernel Online")
        print("[✓] JAOS Ready")

        return True

    def shutdown(self):
        """Shutdown JAOS."""

        self.system_status = "OFFLINE"

        print("[✓] JAOS Shutdown Complete")

    def get_system_status(self):
        """Return current system status."""

        return {
            "version": self.VERSION,
            "status": self.system_status,
            "started_at": self.started_at,
            "registry_manager": self.registry_manager is not None,
        }

    def uptime(self):
        """Return uptime in seconds."""

        if self.started_at is None:
            return 0

        return (datetime.now() - self.started_at).total_seconds()