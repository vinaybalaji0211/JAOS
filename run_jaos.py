from __future__ import annotations

import sys

from jaos.cli.shell import JAOSShell
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

        try:
            JAOSShell().run()
        except Exception:
            logger.exception("Unhandled error in JAOS shell")
            print()
            print("JAOS encountered an unrecoverable error and is shutting down.")
            self.boot_manager.shutdown()
            return 1

        return 0 if self.boot_manager.shutdown() else 1


if __name__ == "__main__":
    sys.exit(JAOSApplication().run())
