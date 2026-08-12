from jaos.cli.shell import JAOSShell
from jaos.version import JAOS_VERSION


class JAOSApplication:
    def boot(self) -> None:
        print("=" * 40)
        print(f"JAOS {JAOS_VERSION}")
        print("Jarvis Artificial Operating System")
        print("=" * 40)
        print()
        print("Boot Complete")
        print()
        print("Good evening, Vinay.")

    def run(self) -> None:
        self.boot()

        shell = JAOSShell()
        shell.run()


if __name__ == "__main__":
    JAOSApplication().run()
