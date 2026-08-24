from __future__ import annotations

import sys

from jaos.cli.command_dispatcher import CommandDispatcher
from jaos.cli.shell import JAOSShell
from jaos.composition import PlatformComposition
from jaos.version import JAOS_VERSION
from jaos_platform.boot_manager import BootManager
from jaos_platform.platform_runtime import PlatformRuntime
from logs.logger import logger


class JAOSApplication:
    """Sole production launcher.

    Owns the one PlatformRuntime composition root and drives its lifecycle
    (initialize/start/stop) around the interactive shell.
    """

    def __init__(self, runtime: PlatformRuntime | None = None) -> None:
        self.runtime = runtime or PlatformRuntime()
        self.boot_manager = BootManager(self.runtime)

    def boot(self) -> None:
        print("=" * 40)
        print(f"JAOS {JAOS_VERSION}")
        print("Jarvis Artificial Operating System")
        print("=" * 40)
        print()
        print("Good evening, Vinay.")

    def run(self) -> int:
        self.boot()

        self.runtime.configure_logging()

        if not self.boot_manager.boot():
            print()
            print("JAOS failed to reach a ready state.")
            self.boot_manager.shutdown()
            return 1

        composition = PlatformComposition(self.runtime)
        composed = False
        shell_ok = False

        try:
            composition.compose()
            composed = True

            dispatcher = CommandDispatcher(
                composition.tool_manager,
                ai_manager=composition.ai_manager,
                executive=composition.executive_controller,
            )
            JAOSShell(dispatcher).run()
            shell_ok = True
        except Exception:
            logger.exception("Unhandled error while composing or running JAOS")
            print()
            print("JAOS encountered an unrecoverable error and is shutting down.")

        teardown_ok = True
        if composed:
            try:
                composition.teardown()
            except Exception:
                logger.exception("Error tearing down composed platforms")
                teardown_ok = False

        runtime_stopped_ok = self.boot_manager.shutdown()

        return 0 if (shell_ok and teardown_ok and runtime_stopped_ok) else 1


if __name__ == "__main__":
    sys.exit(JAOSApplication().run())
