from jaos.cli.shell import JAOSShell


class JAOSApplication:
    def boot(self) -> None:
        print("=" * 40)
        print("JAOS v0.6.0-alpha")
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