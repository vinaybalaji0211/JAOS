from logs.logger import logger


class AuthenticationManager:

    def __init__(self):

        self.methods = {}

    def register_method(
            self,
            username,
            method,
            enabled=True):

        self.methods[username] = {
            "method": method,
            "enabled": enabled
        }

        logger.info(
            f"Authentication registered: {username}"
        )

    def show_methods(self):

        print("\n=== Authentication Manager ===\n")

        if not self.methods:

            print("No authentication methods.")
            return

        for username, data in self.methods.items():

            print(username)
            print(f"  Method  : {data['method']}")
            print(f"  Enabled : {data['enabled']}")
            print()