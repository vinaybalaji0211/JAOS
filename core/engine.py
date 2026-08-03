from core.action_history import ActionHistory
from core.command_system import CommandSystem
from core.config_manager import ConfigManager
from core.diagnostics import Diagnostics
from core.error_handler import ErrorHandler
from core.event_system import EventSystem
from core.health_monitor import HealthMonitor
from core.module_loader import ModuleLoader
from core.plugin_manager import PluginManager
from core.recovery_manager import RecoveryManager
from core.snapshot_manager import SnapshotManager
from core.status_manager import StatusManager
from core.version_manager import VersionManager
from jaos_platform.platform_runtime import PlatformRuntime
from logs.logger import logger
from tests.test_runner import TestRunner


class JarvisEngine:

    def __init__(self, runtime: PlatformRuntime | None = None):

        logger.info("Engine initialized")

        self.runtime = runtime or PlatformRuntime()

        self.module_loader = ModuleLoader()
        self.event_system = EventSystem()
        self.plugin_manager = PluginManager()
        self.status_manager = StatusManager()
        self.config = ConfigManager.load_config()

        self.runtime.container.register("jarvis_engine", self)
        self.runtime.context.set("engine_status", "INITIALIZED")
        self.runtime.events.publish(
            "engine_initialized",
            {"status": "INITIALIZED"}
        )

    def start(self):

        try:

            logger.info("Engine started")

            ActionHistory.record_action("Engine started")

            print(f"{self.config['jarvis_name']} is online.")

            self.module_loader.load_module("Logger")
            ActionHistory.record_action("Logger module loaded")
            self.module_loader.show_modules()

            self.event_system.emit("system_started")
            ActionHistory.record_action("system_started event emitted")
            self.event_system.show_events()

            self.plugin_manager.load_plugins()
            self.plugin_manager.show_plugins()
            ActionHistory.record_action("Plugins loaded")

            TestRunner.run_tests()
            ActionHistory.record_action("System tests completed")

            health = HealthMonitor.get_system_health()

            print("\nSystem Health:")

            for key, value in health.items():
                print(f"{key}: {value}%")

            diagnostics = Diagnostics.run_diagnostics(
                self.module_loader.modules,
                self.event_system.events,
                self.plugin_manager.plugins,
                health
            )

            print("\nDiagnostics Report:\n")

            for key, value in diagnostics.items():
                print(f"{key}: {value}")

            self.status_manager.show_status()
            VersionManager.show_version()

            ActionHistory.record_action("Version information displayed")

            previous_state = RecoveryManager.recover_latest_snapshot()

            if previous_state:
                print("\nRecovered Previous State:")
                print(previous_state)

            SnapshotManager.create_snapshot(
                {
                    "status": self.status_manager.get_status(),
                    "modules": self.module_loader.modules,
                    "events": self.event_system.events,
                    "plugins": self.plugin_manager.plugins,
                    "health": health,
                    "diagnostics": diagnostics,
                    "config": self.config
                }
            )

            SnapshotManager.create_snapshot(
                {
                    "milestone": "PHASE_1_COMPLETE",
                    "version": "0.1"
                }
            )

            ActionHistory.record_action("Snapshot created")

            print("\nInteractive Console Started")

            while True:

                command = input("\nYou: ")

                response = CommandSystem.process(command)

                print("JARVIS:", response)

                ActionHistory.record_action(f"Command: {command}")

                if command.lower() == "exit":
                    break

        except Exception as error:

            ErrorHandler.handle_error(error)