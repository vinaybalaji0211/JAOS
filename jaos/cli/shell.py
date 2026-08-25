from jaos.cli.command_dispatcher import CommandDispatcher


class JAOSShell:
    """
    Interactive command shell for JAOS.
    """

    def __init__(self, dispatcher: CommandDispatcher) -> None:
        if dispatcher is None:
            raise TypeError("dispatcher must not be None")

        self.dispatcher = dispatcher

    def run(self) -> None:
        print()
        print("Type 'help' for available commands.")
        print("Type 'exit' to quit.")
        print()

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
