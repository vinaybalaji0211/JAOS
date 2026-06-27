from logs.logger import logger


class AuthorizationManager:

    def __init__(self):

        self.roles = {}

    def register_role(
            self,
            username,
            role):

        self.roles[username] = role

        logger.info(
            f"Role assigned: {username} -> {role}"
        )

    def is_authorized(
            self,
            username,
            required_role):

        return self.roles.get(username) == required_role

    def show_roles(self):

        print("\n=== Authorization Manager ===\n")

        if not self.roles:

            print("No roles assigned.")
            return

        for username, role in self.roles.items():

            print(f"{username} : {role}")