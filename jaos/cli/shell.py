from jaos.cli.command_dispatcher import CommandDispatcher


class JAOSShell:
    """
    Interactive command shell for JAOS.
    """

    def __init__(self) -> None:
        self.dispatcher = CommandDispatcher()

    def run(self) -> None:
        print()
        print("Type 'help' for available commands.")
        print("Type 'exit' to quit.")
        print()

        try:
            running = True

            while running:
                try:
                    command = input("JAOS > ").strip()
                except EOFError:
                    print()
                    print("Shutting down JAOS...")
                    break

                if not command:
                    continue

                running = self.dispatcher.dispatch(command)
        finally:
            self.dispatcher.shutdown()
